import pandas as pd

# Load the data
data = pd.read_csv('/workspace/mushrooms.csv')

# Display basic information about the dataset
print(data.info())

# Display the first few rows of the dataset
print(data.head())

# Check for any missing values
print(data.isnull().sum())

# Check the distribution of the class labels
print(data['class'].value_counts())
