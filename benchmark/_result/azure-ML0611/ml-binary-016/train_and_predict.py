import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# Load the dataset
data = pd.read_csv('/workspace/UCI_Credit_Card.csv')

# Prepare the data for training
X = data.drop(['ID', 'default.payment.next.month'], axis=1)
y = data['default.payment.next.month']

# Split the data into training and validation sets
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize the model
model = RandomForestClassifier(n_estimators=100, random_state=42)

# Train the model
model.fit(X_train, y_train)

# Validate the model
y_pred_val = model.predict(X_val)
accuracy = accuracy_score(y_val, y_pred_val)
print(f"Validation Accuracy: {accuracy}")

# Load the test data
test_data = pd.read_csv('/workspace/test.csv')

# Prepare the test data
X_test = test_data.drop(['ID'], axis=1)

# Make predictions on the test data
test_data['IsDefaulter'] = model.predict(X_test)

# Save the predictions to a CSV file
test_data[['ID', 'IsDefaulter']].to_csv('/workspace/defaulter.csv', index=False)
