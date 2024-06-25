import pandas as pd

# Load the concatenated CSV file with explicit data types for columns with mixed types
dtype_dict = {
    'Permit Number': 'float64',  # Assuming float due to mixed types, will convert to int later
    'Structural Notification': 'object',  # Mixed types suggest it should be treated as object
    'Voluntary Soft-Story Retrofit': 'object',
    'Fire Only Permit': 'object',
    'TIDF Compliance': 'object',
    'Site Permit': 'object',
    'Permit Number': 'object',  # Duplicate column name, treating as object
    'Permit Type': 'object',  # Duplicate column name, treating as object
    'Permit_Creation_Date': 'object',  # Duplicate column name, treating as object
    'Proposed_Units': 'float64',  # Assuming float due to mixed types
    'permit Type': 'object',  # Duplicate column name, treating as object
    'permit_Number': 'object',  # Duplicate column name, treating as object
    'Structural_Notification': 'object'  # Duplicate column name, treating as object
}
df = pd.read_csv('/workspace/concatenated_permits.csv', dtype=dtype_dict, low_memory=False)

# Check for missing values and print the count of missing values per column
missing_values_count = df.isnull().sum()
print("Missing values per column:\n", missing_values_count)

# Define a function to fill missing values with the mode of the group
def fill_with_mode(group):
    modes = group.mode()
    if modes.empty:
        return group
    else:
        return group.fillna(modes.iloc[0])

# Apply the function to each column, grouping by 'Street Name' and 'Block'
for column in df.columns:
    try:
        df[column] = df.groupby(['Street Name', 'Block'])[column].transform(fill_with_mode)
    except Exception as e:
        print(f"Error processing column {column}: {e}")

# Convert 'Permit Number' back to int after filling missing values
df['Permit Number'] = df['Permit Number'].fillna(0).astype(int)

# Save the cleaned DataFrame to a new CSV file
df.to_csv('/workspace/Building_Permits.csv', index=False)
print("Missing values filled and cleaned data saved to Building_Permits.csv.")
