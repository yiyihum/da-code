import pandas as pd

# Load the dataset
df = pd.read_csv('/workspace/New_York_cars.csv')

# Display basic information about the dataset
print(df.info())

# Display the first few rows of the dataset to understand the data better
print(df.head())
