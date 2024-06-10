import pandas as pd

# Load the dataset
data = pd.read_csv('/workspace/test.csv')

# Display basic information about the dataset
print(data.info())
print(data.describe())

# Check for missing values
print(data.isnull().sum())
