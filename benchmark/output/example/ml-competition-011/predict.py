import pandas as pd
import joblib

# Load the test data
test_data = pd.read_csv('test.csv')

# Load the model from the file
model = joblib.load('model.joblib')

# Make predictions on the test data
predictions = model.predict(test_data.drop('id', axis=1))

# Create a DataFrame for the submission
submission = pd.DataFrame({'id': test_data['id'], 'yield': predictions})

# Write the submission DataFrame to a CSV file
submission.to_csv('submission.csv', index=False)
