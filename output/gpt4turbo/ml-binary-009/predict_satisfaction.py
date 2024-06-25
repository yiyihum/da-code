import pandas as pd
import joblib

# Load the trained model
model = joblib.load('/workspace/passenger_satisfaction_model.joblib')

# Load the test data
test_data = pd.read_csv('/workspace/test.csv')

# Preprocessing
# Drop the 'Unnamed: 0' and 'id' columns as they are not features
test_data.drop(['Unnamed: 0', 'id'], axis=1, inplace=True)

# Convert categorical variables to dummy variables
test_data = pd.get_dummies(test_data, drop_first=True)

# Ensure the test data has the same feature columns as the training data
# This step is important to handle any categorical levels that might be missing in the test data
train_data = pd.read_csv('/workspace/train.csv')
train_data.drop(['Unnamed: 0', 'id'], axis=1, inplace=True)
train_data = pd.get_dummies(train_data, drop_first=True)
test_data = test_data.reindex(columns=train_data.drop('satisfaction_satisfied', axis=1).columns, fill_value=0)

# Predict satisfaction
predictions = model.predict(test_data)

# Map the boolean predictions to strings
predictions_mapped = ['satisfied' if pred else 'neutral or dissatisfied' for pred in predictions]

# Save the mapped predictions to a CSV file
result = pd.DataFrame(predictions_mapped, columns=['satisfaction'])
result.to_csv('/workspace/result.csv', index=False)
