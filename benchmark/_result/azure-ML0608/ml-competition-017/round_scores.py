import pandas as pd

# Load the submission file
submission_df = pd.read_csv('/workspace/submission.csv')

# Round the scores to the nearest integer
submission_df['score'] = submission_df['score'].round().astype(int)

# Save the updated submission file
submission_df.to_csv('/workspace/submission.csv', index=False)
