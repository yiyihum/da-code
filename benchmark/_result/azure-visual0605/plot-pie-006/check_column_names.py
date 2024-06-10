import pandas as pd

# Load the dataset with low_memory=False to address the DtypeWarning
df = pd.read_csv('/workspace/scrubbed.csv', low_memory=False)

# Output the column names to check the correct column name for the country
print(df.columns.tolist())
