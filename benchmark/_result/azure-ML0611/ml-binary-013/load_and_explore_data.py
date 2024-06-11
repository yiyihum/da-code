import pandas as pd

# Load the training data
train_data = pd.read_csv('/workspace/Train.csv')

# Display basic information about the dataset
print(train_data.info())

# Display statistical summary of the features
print(train_data.describe())

# Check for missing values
print(train_data.isnull().sum())

# Display the first few rows of the dataset
print(train_data.head())
