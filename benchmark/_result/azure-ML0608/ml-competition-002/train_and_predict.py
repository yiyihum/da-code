import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score

# Load the training data
train_data = pd.read_csv('/workspace/train.csv')

# Separate features and target
X = train_data.drop(columns=['id', 'smoking'])
y = train_data['smoking']

# Split the data into training and validation sets
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize the logistic regression model
model = LogisticRegression(max_iter=1000)

# Train the model
model.fit(X_train, y_train)

# Validate the model
y_val_pred = model.predict_proba(X_val)[:, 1]
val_auc = roc_auc_score(y_val, y_val_pred)
print(f'Validation AUC: {val_auc}')

# Load the test data
test_data = pd.read_csv('/workspace/test.csv')

# Keep the ID for submission
test_ids = test_data['id']

# Make predictions on the test data
X_test = test_data.drop(columns=['id'])
test_predictions = model.predict_proba(X_test)[:, 1]

# Create the submission file
submission = pd.DataFrame({'id': test_ids, 'smoking': test_predictions})
submission.to_csv('/workspace/submission.csv', index=False)
print('Submission file created.')
