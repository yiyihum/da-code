import pandas as pd

# Load the dataset
df = pd.read_csv('/workspace/test.csv')

# Check for missing values
missing_values = df.isnull().sum()

# Output the missing values to a CSV file for review
missing_values.to_csv('/workspace/missing_values.csv', header=True)

# Print the first few rows of the dataframe
print(df.head())

# Print the missing values
print(missing_values)
