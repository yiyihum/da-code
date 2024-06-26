import pandas as pd

# Load the CSV files into DataFrames
df1 = pd.read_csv('/workspace/Building_Permits_1.csv')
df2 = pd.read_csv('/workspace/Building_Permits_2.csv')
df3 = pd.read_csv('/workspace/Building_Permits_3.csv')
df4 = pd.read_csv('/workspace/Building_Permits_4.csv')

# Combine the DataFrames into a single DataFrame
df = pd.concat([df1, df2, df3, df4], ignore_index=True)

# Clean the column names to match the schema
# Remove any duplicate or unnecessary columns
df = df.loc[:, ~df.columns.duplicated()]
df.columns = df.columns.str.replace(' ', '_')  # Replace spaces with underscores
df.columns = df.columns.str.replace(r'(?<!^)(?=[A-Z])', '_').str.lower()  # Convert camelCase to snake_case

# Preview the cleaned column names
print(df.columns.tolist())
