import pandas as pd

# Load the dataset
df = pd.read_csv('/workspace/data.csv')

# Display the first few rows of the dataframe
print(df.head())

# Check for missing values in each column
print(df.isnull().sum())
