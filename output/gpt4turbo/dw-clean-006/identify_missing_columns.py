import pandas as pd

# Load the concatenated CSV file
df = pd.read_csv('/workspace/concatenated_permits.csv', low_memory=False)

# Identify columns with missing values
missing_columns = df.columns[df.isnull().any()].tolist()

# Save the list of columns with missing values to a CSV file for reference
pd.Series(missing_columns).to_csv('/workspace/missing_columns.csv', index=False, header=False)
print("List of columns with missing values saved to missing_columns.csv.")
