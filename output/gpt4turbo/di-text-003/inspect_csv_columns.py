import pandas as pd

# Load the data
df = pd.read_csv('/workspace/world-data-2023.csv')

# Print the column names to find out the correct column for birth rate
print(df.columns.tolist())
