import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# Load the training data
train_data = pd.read_csv('/workspace/train.csv')

# Preprocessing
# Drop the 'Unnamed: 0' and 'id' columns as they are not features
train_data.drop(['Unnamed: 0', 'id'], axis=1, inplace=True)

# Convert categorical variables to dummy variables
train_data = pd.get_dummies(train_data, drop_first=True)

# Separate features and target
X = train_data.drop('satisfaction_satisfied', axis=1)
y = train_data['satisfaction_satisfied']

# Split the data into training and validation sets
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the model
model = RandomForestClassifier(random_state=42)
model.fit(X_train, y_train)

# Validate the model
y_pred = model.predict(X_val)
accuracy = accuracy_score(y_val, y_pred)
print(f"Validation accuracy: {accuracy}")

# Save the model to a file
import joblib
joblib.dump(model, '/workspace/passenger_satisfaction_model.joblib')
