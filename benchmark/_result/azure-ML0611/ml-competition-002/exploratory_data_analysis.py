import pandas as pd

# Load the datasets
train_df = pd.read_csv('/workspace/train.csv')
test_df = pd.read_csv('/workspace/test.csv')
extra_train_df = pd.read_csv('/workspace/test_dataset.csv')

# Display basic information about the datasets
print("Train dataset info:")
print(train_df.info())
print("\nTest dataset info:")
print(test_df.info())
print("\nExtra train dataset info:")
print(extra_train_df.info())

# Display the first few rows of the datasets
print("\nTrain dataset head:")
print(train_df.head())
print("\nTest dataset head:")
print(test_df.head())
print("\nExtra train dataset head:")
print(extra_train_df.head())

# Check for missing values in the datasets
print("\nMissing values in train dataset:")
print(train_df.isnull().sum())
print("\nMissing values in test dataset:")
print(test_df.isnull().sum())
print("\nMissing values in extra train dataset:")
print(extra_train_df.isnull().sum())
