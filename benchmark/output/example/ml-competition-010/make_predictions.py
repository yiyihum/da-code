import pandas as pd
import joblib

# Load the trained model and the encoder from the files
model = joblib.load('model.joblib')
encoder = joblib.load('encoder.joblib')

# Load the test dataset
test = pd.read_csv('test.csv')

# Transform the 'Sex' column of the test dataset
test_encoded = pd.DataFrame(encoder.transform(test[['Sex']]).toarray())

# Replace the 'Sex' column with the encoded data
test = test.drop('Sex', axis=1)
test = pd.concat([test, test_encoded], axis=1)

# Convert all feature names to strings
test.columns = test.columns.astype(str)

# Make predictions on the test dataset
test_predictions = model.predict(test)

# Create a DataFrame for the submission
submission = pd.DataFrame({'id': test['id'], 'Age': test_predictions})

# Write the submission DataFrame to a CSV file
submission.to_csv('submission.csv', index=False)
