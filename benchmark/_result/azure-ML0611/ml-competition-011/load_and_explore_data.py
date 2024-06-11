import pandas as pd

# Load the datasets
train_df = pd.read_csv('/workspace/train.csv')
test_df = pd.read_csv('/workspace/test.csv')
sample_submission_df = pd.read_csv('/workspace/sample_submission.csv')
ffs_df = pd.read_csv('/workspace/ffs.csv')

# Display the first few rows of the datasets
print("Train DataFrame head:")
print(train_df.head())
print("\nTest DataFrame head:")
print(test_df.head())
print("\nSample Submission DataFrame head:")
print(sample_submission_df.head())
print("\nFFS DataFrame head:")
print(ffs_df.head())

# Display summary statistics of the training data
print("\nTrain DataFrame description:")
print(train_df.describe())

# Check for missing values in the training and test data
print("\nMissing values in Train DataFrame:")
print(train_df.isnull().sum())
print("\nMissing values in Test DataFrame:")
print(test_df.isnull().sum())
