import pandas as pd

# Load the test data
test_df = pd.read_csv('/workspace/test.csv')

# Placeholder for model predictions (since we don't have a model yet)
# This is just a placeholder and should be replaced with actual model predictions
test_df['score'] = 3  # Assuming a default score for demonstration

# Save the predictions to a submission file
submission_df = test_df[['essay_id', 'score']]
submission_df.to_csv('/workspace/submission.csv', index=False)
