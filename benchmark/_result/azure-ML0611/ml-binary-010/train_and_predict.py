import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# Load the training data
train_data = pd.read_csv('/workspace/heart.csv')

# Separate features and target
X = train_data.drop('output', axis=1)
y = train_data['output']

# Split the data into training and validation sets
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize the model
model = RandomForestClassifier(n_estimators=100, random_state=42)

# Train the model
model.fit(X_train, y_train)

# Validate the model
y_pred_val = model.predict(X_val)
val_accuracy = accuracy_score(y_val, y_pred_val)
print(f"Validation Accuracy: {val_accuracy}")

# Load the test data
test_data = pd.read_csv('/workspace/test.csv')

# Make predictions on the test data
predictions = model.predict(test_data)

# Save the predictions to result.csv
result_df = pd.DataFrame(predictions, columns=['output'])
result_df.to_csv('/workspace/result.csv', index=False)
