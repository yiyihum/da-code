import pandas as pd

# Load the test essays data
test_essays = pd.read_csv('/workspace/test_essays.csv')

# Placeholder for predictions (for demonstration purposes, using a fixed probability)
# In a real scenario, this would involve text preprocessing and a trained model to make predictions.
test_essays['generated'] = 0.5  # This is a dummy value and should be replaced with actual model predictions.

# Save the predictions to submission.csv
submission = test_essays[['id', 'generated']]
submission.to_csv('/workspace/submission.csv', index=False)
