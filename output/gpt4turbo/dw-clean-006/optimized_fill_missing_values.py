import pandas as pd

# Load the concatenated CSV file
df = pd.read_csv('/workspace/concatenated_permits.csv', low_memory=False)

# Define a function to fill missing values with the mode of the group
def fill_with_mode(df, column, group_columns):
    # Compute the mode for each group
    mode_series = df.groupby(group_columns)[column].apply(lambda x: x.mode().iloc[0] if not x.mode().empty else None)
    # Create a dictionary mapping from the group to the mode value
    mode_mapping = mode_series.to_dict()
    
    # Define a function to apply the mapping
    def fill_mode(row):
        group_key = tuple(row[group_columns])
        return row[column] if pd.notnull(row[column]) else mode_mapping.get(group_key, None)
    
    # Fill missing values using the mapping
    df[column] = df.apply(fill_mode, axis=1)

# List of columns to fill with mode, excluding columns with unique identifiers or descriptions
columns_to_fill = df.columns.difference(['Permit Number', 'Description', 'Record ID'])

# Apply the function to each column that needs missing values filled
for column in columns_to_fill:
    fill_with_mode(df, column, ['Street Name', 'Block'])

# Save the cleaned DataFrame to a new CSV file
df.to_csv('/workspace/Building_Permits.csv', index=False)
print("Missing values filled and cleaned data saved to Building_Permits.csv.")
