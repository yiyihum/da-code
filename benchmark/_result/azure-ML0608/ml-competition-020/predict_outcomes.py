import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import f1_score
from sklearn.preprocessing import LabelEncoder

# Load the training data
train_data = pd.read_csv('/workspace/train.csv')

# Preprocess the data: Fill missing values and convert categorical to numerical
train_data.fillna(method='ffill', inplace=True)
label_encoders = {}
for column in train_data.columns:
    if train_data[column].dtype == object:
        le = LabelEncoder()
        train_data[column] = le.fit_transform(train_data[column])
        label_encoders[column] = le

# Separate features and target
X = train_data.drop(['id', 'outcome'], axis=1)
y = train_data['outcome']

# Split the data into training and validation sets
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

# Train a Random Forest Classifier
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Validate the model
y_pred = model.predict(X_val)
f1 = f1_score(y_val, y_pred, average='micro')
print(f'Validation F1 Score: {f1}')

# Load the test data
test_data = pd.read_csv('/workspace/test.csv')
test_ids = test_data['id']

# Preprocess the test data using the same approach as for the training data
for column in test_data.columns:
    if test_data[column].dtype == object:
        le = label_encoders.get(column)
        if le:
            test_data[column] = le.transform(test_data[column].fillna(method='ffill'))

# Drop 'id' column and make predictions
X_test = test_data.drop('id', axis=1)
test_predictions = model.predict(X_test)

# Create the submission file
submission = pd.DataFrame({'id': test_ids, 'outcome': test_predictions})
submission['outcome'] = submission['outcome'].map(lambda x: label_encoders['outcome'].inverse_transform([x])[0])
submission.to_csv('/workspace/submission.csv', index=False)
