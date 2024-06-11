import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# Load the training data
train_data = pd.read_csv('/workspace/train.csv')
train_data.drop(['id', 'Unnamed: 32'], axis=1, inplace=True)

# Separate features and target
X = train_data.drop('diagnosis', axis=1)
y = train_data['diagnosis']

# Split the data into training and validation sets
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize the model
model = RandomForestClassifier(n_estimators=100, random_state=42)

# Train the model
model.fit(X_train, y_train)

# Validate the model
y_pred = model.predict(X_val)
accuracy = accuracy_score(y_val, y_pred)
print(f"Validation accuracy: {accuracy}")

# Load the test data
test_data = pd.read_csv('/workspace/test.csv')
test_data.drop(['id', 'Unnamed: 32'], axis=1, inplace=True)

# Predict using the trained model
test_predictions = model.predict(test_data)

# Write the predictions to a CSV file
prediction_df = pd.DataFrame(test_predictions, columns=['result'])
prediction_df.to_csv('/workspace/label.csv', index=False)
