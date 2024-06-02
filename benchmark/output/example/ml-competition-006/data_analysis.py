import pandas as pd

# Load the training data
train_data = pd.read_csv('train.csv')

# Display the first few rows of the data
print(train_data.head())

# Display the summary statistics of the data
print(train_data.describe())

# Check for missing values
print(train_data.isnull().sum())
