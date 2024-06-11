import pandas as pd

# Load the dataset with the correct delimiter
df = pd.read_csv('/workspace/marketing_campaign.csv', delimiter='\t')

# Display basic information about the dataset
print(df.info())

# Display the first few rows of the dataset to understand its structure
print(df.head())
