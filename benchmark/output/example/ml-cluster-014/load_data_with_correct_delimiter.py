import pandas as pd

# Load the dataset with the correct delimiter
df = pd.read_csv('/workspace/marketing_campaign.csv', delimiter='\t')

# Display basic information about the dataset with the correct delimiter
print(df.info())
print(df.head())
