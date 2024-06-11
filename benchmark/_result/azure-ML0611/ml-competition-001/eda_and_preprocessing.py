import pandas as pd

# Load the training data
train_df = pd.read_csv('/workspace/train.csv')

# Display basic information about the dataset
print(train_df.info())

# Display statistical summary of numerical features
print(train_df.describe())

# Check for missing values
print(train_df.isnull().sum())

# Display the first few rows of the dataset
print(train_df.head())
