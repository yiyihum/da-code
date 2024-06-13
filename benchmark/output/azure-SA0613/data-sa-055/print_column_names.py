import pandas as pd

# Load the dataset
df = pd.read_csv('frog_tongue.csv', comment='#')

# Print the column names to identify the relevant columns for Frog B and Frog D
print(df.columns.tolist())
