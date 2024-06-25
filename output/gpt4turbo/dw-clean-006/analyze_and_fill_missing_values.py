import pandas as pd

# Load the concatenated CSV file
df = pd.read_csv('/workspace/concatenated_permits.csv')

# Check for missing values and print the count of missing values per column
missing_values_count = df.isnull().sum()
print("Missing values per column:\n", missing_values_count)

# Define a function to fill missing values with the mode of the group
def fill_with_mode(group):
    modes = group.mode()
    return group.fillna(modes.iloc[0])

# Apply the function to each column, grouping by 'Street Name' and 'Block'
for column in df.columns:
    df[column] = df.groupby(['Street Name', 'Block'])[column].transform(fill_with_mode)

# Save the cleaned DataFrame to a new CSV file
df.to_csv('/workspace/Building_Permits.csv', index=False)
print("Missing values filled and cleaned data saved to Building_Permits.csv.")
