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

# Remove duplicate columns by keeping the first occurrence
df = df.loc[:, ~df.columns.duplicated(keep='first')]

# Fill missing values using the mode within each group defined by Street Name and Block
for column in df.columns:
    # Skip columns that do not have missing values or are not relevant for mode imputation
    if df[column].isnull().sum() == 0 or column in ['street_name', 'block']:
        continue
    # Group by 'street_name' and 'block', then transform each group by filling missing values with the mode
    df[column] = df.groupby(['street_name', 'block'])[column].transform(lambda x: x.fillna(x.mode()[0] if not x.mode().empty else x))

# Save the cleaned DataFrame to a CSV file
df.to_csv('/workspace/Building_Permits.csv', index=False)
