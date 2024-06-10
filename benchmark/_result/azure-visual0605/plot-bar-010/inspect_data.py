import pandas as pd

# Load the dataset
data = pd.read_csv('/workspace/data.csv')

# Display the first few rows of the dataframe
print(data.head())

# Display the data types of each column to identify categorical and numerical features
print(data.dtypes)
