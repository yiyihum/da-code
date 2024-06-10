import pandas as pd

# Load the dataset
df = pd.read_csv('/workspace/online_retail_II.csv')

# Display basic information about the dataset
print(df.info())
print(df.head())
