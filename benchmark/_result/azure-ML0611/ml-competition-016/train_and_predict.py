import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# Load the training data
train_data = pd.read_csv('/workspace/train.csv')

# Preprocess the data: drop non-numeric columns and the 'id' column
X = train_data.drop(columns=['id', 'Product ID', 'Type', 'Machine failure'])
y = train_data['Machine failure']

# Split the data into training and validation sets
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize the Random Forest classifier
rf_clf = RandomForestClassifier(n_estimators=100, random_state=42)

# Train the classifier
rf_clf.fit(X_train, y_train)

# Validate the classifier
y_pred_val = rf_clf.predict(X_val)
val_accuracy = accuracy_score(y_val, y_pred_val)
print(f"Validation Accuracy: {val_accuracy}")

# Load the test data
test_data = pd.read_csv('/workspace/test.csv')

# Preprocess the test data: drop non-numeric columns and the 'id' column, keep 'id' for submission
X_test = test_data.drop(columns=['Product ID', 'Type', 'id'])
test_ids = test_data['id']

# Make predictions on the test data
test_predictions = rf_clf.predict_proba(X_test)[:, 1]

# Create the submission dataframe
submission = pd.DataFrame({'id': test_ids, 'Machine failure': test_predictions})

# Save the submission file
submission.to_csv('/workspace/submission.csv', index=False)
