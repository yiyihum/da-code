import pandas as pd

# Load the datasets
test_data = pd.read_csv('/workspace/test.csv')
sample_submission = pd.read_csv('/workspace/sample_submission.csv')

# Print the lengths of the test data and the sample submission
print("Length of test data:", len(test_data))
print("Length of sample submission:", len(sample_submission))
