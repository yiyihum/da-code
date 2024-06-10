import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler

# Load the training data
train_data = pd.read_csv('/workspace/train.csv')

# Separate features and target
X_train = train_data.drop(columns=['id', 'smoking'])
y_train = train_data['smoking']

# Scale the features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)

# Initialize the logistic regression model with increased max_iter
model = LogisticRegression(max_iter=10000)

# Train the model
model.fit(X_train_scaled, y_train)

# Load the test data
test_data = pd.read_csv('/workspace/test.csv')

# Scale the test data using the same scaler
X_test_scaled = scaler.transform(test_data)

# Make predictions on the test data
test_predictions = model.predict_proba(X_test_scaled)[:, 1]

# Generate 'id' column for the test data based on the training data 'id' range
min_id = train_data['id'].min()
test_ids = range(min_id, min_id + len(test_data))

# Create the submission file
submission = pd.DataFrame({'id': test_ids, 'smoking': test_predictions})
submission.to_csv('/workspace/submission.csv', index=False)
print('Submission file created.')
