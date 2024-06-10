import pandas as pd

# Load the dataset
df = pd.read_csv('/workspace/customer_segmentation.csv')

# Display basic information about the dataset
print(df.info())

# Display the first few rows of the dataset
print(df.head())

# Check for missing values
print(df.isnull().sum())
