import pandas as pd

# Load the trained model
model_filename = '/workspace/microbusiness_model.pkl'
model = pd.read_pickle(model_filename)

# Load the test data
test_data = pd.read_csv('/workspace/test.csv')

# Preprocess the test data: Here we'll just use the 'active' feature as we did for training
X_test = test_data[['active']]

# Make predictions
test_data['microbusiness_density'] = model.predict(X_test)

# Prepare the submission file
submission = test_data[['row_id', 'microbusiness_density']]
submission_filename = '/workspace/submission.csv'
submission.to_csv(submission_filename, index=False)
print(f"Submission file saved to {submission_filename}")
