import pandas as pd

# Load the dataset
data = pd.read_csv('Country-data.csv')

# Display the first few rows of the dataframe
print(data.head())

# Display the summary statistics and information about the dataset
print(data.describe())
print(data.info())
