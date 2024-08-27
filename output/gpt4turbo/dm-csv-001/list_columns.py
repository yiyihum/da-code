import pandas as pd

# Load the dataset
df = pd.read_csv('/workspace/ufc-fighters-statistics.csv')

# Print all column names to identify the relevant ones for weight class and fight record
print(df.columns.tolist())
