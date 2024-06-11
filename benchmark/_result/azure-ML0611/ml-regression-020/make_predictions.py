import pandas as pd
import joblib

# Load the preprocessed test data and the trained model
test_data = pd.read_csv('/workspace/test_preprocessed.csv')
model = joblib.load('/workspace/delivery_time_predictor.joblib')

# Make predictions on the test set
predictions = model.predict(test_data)

# Generate a sequential ID for the submission file
submission_ids = ['0x' + format(i, 'x') for i in range(len(predictions))]

# Create the submission file
submission = pd.DataFrame({
    'ID': submission_ids,
    'Time_taken (min)': predictions
})
submission.to_csv('/workspace/submission.csv', index=False)

# Output the first few lines of the submission file to verify the format
print(submission.head())
