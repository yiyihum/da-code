import pandas as pd

# Load the dataset
data = pd.read_csv('/workspace/marketing_campaign.csv')

# Display basic information about the dataset
print(data.info())

# Display the first few rows of the dataset to understand its structure
print(data.head())
