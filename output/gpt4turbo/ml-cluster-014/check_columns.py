import pandas as pd

# Load the dataset
data = pd.read_csv('marketing_campaign.csv')

# Print the column names
print(data.columns.tolist())
