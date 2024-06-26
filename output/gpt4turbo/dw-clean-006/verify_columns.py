import pandas as pd

# Load the partially cleaned DataFrame
df = pd.read_csv('/workspace/Building_Permits_partial.csv', low_memory=False)

# Output the column names to verify the presence of the 'unit' column and others
print(df.columns.tolist())
