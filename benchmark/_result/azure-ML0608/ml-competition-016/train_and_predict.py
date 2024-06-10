import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import OneHotEncoder

# Load the training data
train_data = pd.read_csv('/workspace/train.csv')

# One-hot encode the 'Type' feature and drop 'Product ID'
train_data = pd.get_dummies(train_data, columns=['Type'], drop_first=True)
train_data.drop('Product ID', axis=1, inplace=True)

# Separate features and target
X = train_data.drop(['id', 'Machine failure'], axis=1)
y = train_data['Machine failure']

# Train the Random Forest model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X, y)

# Load the test data
test_data = pd.read_csv('/workspace/test.csv')

# Apply the same preprocessing to the test data
test_data = pd.get_dummies(test_data, columns=['Type'], drop_first=True)
test_data.drop('Product ID', axis=1, inplace=True)

# Predict using the trained model
test_data['Machine failure'] = model.predict_proba(test_data.drop('id', axis=1))[:, 1]

# Prepare the submission file
submission = test_data[['id', 'Machine failure']]
submission.to_csv('/workspace/submission.csv', index=False)
