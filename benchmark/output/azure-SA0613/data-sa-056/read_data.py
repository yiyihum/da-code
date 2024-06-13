import pandas as pd

# Load the dataset, skipping the initial rows with comments
df = pd.read_csv('frog_tongue.csv', comment='#')

# Display the first few rows of the dataframe to understand its structure
print(df.head())
