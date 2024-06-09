import pandas as pd

# Load the dataset
df = pd.read_csv('/workspace/marketing_campaign.csv')

# Display basic information about the dataset
print(df.info())
print(df.head())
