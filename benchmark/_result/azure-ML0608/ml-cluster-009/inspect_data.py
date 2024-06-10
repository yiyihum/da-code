import pandas as pd

# Load the dataset
df = pd.read_csv('/workspace/world-data-2023.csv')

# Display the first few rows of the dataframe
print(df.head())

# Display the data types of each column
print(df.dtypes)
