import pandas as pd

# Load the dataset
df = pd.read_csv('world-data-2023.csv')

# Print the column names
print(df.columns.tolist())
