import pandas as pd

# Load the test data
test_data = pd.read_csv('/workspace/test.csv')

# Keep the 'id' column to use in the submission file
test_ids = test_data['id']

# Drop the 'id' column as it's not a feature for prediction
X_test = test_data.drop(columns=['id'])

# Use the trained model to predict the 'FloodProbability' on the test set
test_predictions = model.predict(X_test)

# Create a submission DataFrame
submission = pd.DataFrame({
    'id': test_ids,
    'FloodProbability': test_predictions
})

# Save the submission file
submission.to_csv('/workspace/submission.csv', index=False)

# Display the first few lines of the submission file
print(submission.head())
