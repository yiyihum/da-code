import pandas as pd

# Load the test data
test_data = pd.read_csv('/workspace/test.csv')

# Load the trained model
model_filename = '/workspace/flood_prediction_model.pkl'
model = pd.read_pickle(model_filename)

# Make predictions on the test data
test_features = test_data.drop(columns=['id'])
predictions = model.predict(test_features)

# Create the submission dataframe
submission = pd.DataFrame({
    'id': test_data['id'],
    'FloodProbability': predictions
})

# Save the submission file
submission_filename = '/workspace/submission.csv'
submission.to_csv(submission_filename, index=False)
