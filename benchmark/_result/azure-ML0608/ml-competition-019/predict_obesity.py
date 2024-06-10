import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import LabelEncoder

# Load the datasets
train_data = pd.read_csv('/workspace/train.csv')
test_data = pd.read_csv('/workspace/test.csv')

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
test_data['NObeyesdad'] = model.predict(test_data.drop('NObeyesdad', axis=1))

# Create submission file
submission = test_data[['id', 'NObeyesdad']]
submission.to_csv('/workspace/submission.csv', index=False)
