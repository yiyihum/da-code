import pandas as pd

# Load the dataset
df = pd.read_csv('/workspace/Facebook_Live.csv')

# Display the first few rows of the dataframe
print(df.head())

# Display the summary statistics of the dataframe
print(df.describe())

# Check for any missing values
print(df.isnull().sum())
