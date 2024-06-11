import pandas as pd
import numpy as np

# Load the test data to get the Ids
test_data = pd.read_csv('/workspace/test.csv')

# Create a dummy submission with random probabilities
np.random.seed(42)  # For reproducibility
dummy_probabilities = np.random.rand(len(test_data), 2)
dummy_probabilities /= dummy_probabilities.sum(axis=1)[:, None]  # Normalize to sum to 1

# Create a submission dataframe
submission = pd.DataFrame({
    'Id': test_data['Id'],
    'class_0': dummy_probabilities[:, 0],
    'class_1': dummy_probabilities[:, 1]
})

# Save the submission file
submission.to_csv('/workspace/submission.csv', index=False)

# Output the path to the submission file
print("/workspace/submission.csv")
