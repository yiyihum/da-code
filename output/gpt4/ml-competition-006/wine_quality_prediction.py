import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# Load the training data
train_data = pd.read_csv('/workspace/train.csv')

# Separate features and target
X = train_data.drop(columns=['Id', 'quality'])
y = train_data['quality']

# Split the data into training and validation sets
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize the model
model = RandomForestClassifier(random_state=42)

# Train the model
model.fit(X_train, y_train)

# Validate the model
y_pred_val = model.predict(X_val)
val_accuracy = accuracy_score(y_val, y_pred_val)
print(f"Validation Accuracy: {val_accuracy}")

# Load the test data
test_data = pd.read_csv('/workspace/test.csv')

# Predict on the test data
X_test = test_data.drop(columns=['Id'])
test_predictions = model.predict(X_test)

# Create a submission dataframe
submission = pd.DataFrame({
    'Id': test_data['Id'],
    'quality': test_predictions
})

# Save the submission file
submission.to_csv('/workspace/submission.csv', index=False)
