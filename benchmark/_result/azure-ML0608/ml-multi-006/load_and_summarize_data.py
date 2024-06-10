import pandas as pd

# Load the training data
train_data = pd.read_csv('/workspace/train.csv')

# Display basic information about the dataset
print(train_data.info())

# Display summary statistics of the dataset
print(train_data.describe(include='all'))

# Display the first few rows of the dataset
print(train_data.head())
