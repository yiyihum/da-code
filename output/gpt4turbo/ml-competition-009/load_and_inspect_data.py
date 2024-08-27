import pandas as pd

# Load the datasets
train_df = pd.read_csv('/workspace/train.csv')
test_df = pd.read_csv('/workspace/test.csv')
sample_submission_df = pd.read_csv('/workspace/sample_submission.csv')

# Display the first few rows of each dataframe
print("Train DataFrame head:")
print(train_df.head())
print("\nTest DataFrame head:")
print(test_df.head())
print("\nSample Submission DataFrame head:")
print(sample_submission_df.head())

# Check for any missing values in the train and test sets
print("\nMissing values in train set:")
print(train_df.isnull().sum())
print("\nMissing values in test set:")
print(test_df.isnull().sum())

# Summary statistics for the training data
print("\nTrain DataFrame description:")
print(train_df.describe())
