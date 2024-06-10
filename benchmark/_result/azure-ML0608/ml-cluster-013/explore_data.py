import pandas as pd

# Load the dataset
data = pd.read_csv('/workspace/Country-data.csv')

# Display basic information about the dataset
print(data.info())

# Display statistical summary of the dataset
print(data.describe())

# Check for missing values
print(data.isnull().sum())
