import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder

# Load the datasets
train_data = pd.read_csv('/workspace/train.csv')
test_data = pd.read_csv('/workspace/test.csv')

# Remove the extra 'NObeyesdad.1' column from the training data
train_data = train_data.drop(columns=['NObeyesdad.1'], axis=1)

# Separate features and target from training data
X_train = train_data.drop('NObeyesdad', axis=1)
y_train = train_data['NObeyesdad']

# Encode categorical variables
label_encoders = {}
for column in X_train.columns:
    if X_train[column].dtype == 'object':
        le = LabelEncoder()
        X_train[column] = le.fit_transform(X_train[column])
        test_data[column] = le.transform(test_data[column])
        label_encoders[column] = le

# Train the model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Predict on test data
predictions = model.predict(test_data)

# Create submission file
submission = pd.DataFrame({'id': test_data.index, 'NObeyesdad': predictions})
submission.to_csv('/workspace/submission.csv', index=False)
