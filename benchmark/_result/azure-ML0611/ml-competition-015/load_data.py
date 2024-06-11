import pandas as pd

# Load the training data
train_data = pd.read_csv('/workspace/train.csv')

# Display basic information about the dataset
print(train_data.info())
print(train_data.describe())

# Check for any missing values
print(train_data.isnull().sum())
