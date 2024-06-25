import pandas as pd

# Load the updated CSV file with some missing values already filled
df = pd.read_csv('/workspace/concatenated_permits_filled.csv', low_memory=False)

# Load the list of columns with missing values
with open('/workspace/missing_columns.csv', 'r') as file:
    missing_columns = file.read().splitlines()

# Function to fill missing values with the mode of the group
def fill_with_mode(df, column, group_columns):
    # Skip if the column has no missing values
    if df[column].isnull().sum() == 0:
        return df
    
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
    return df

# Fill missing values for the next column in the list
if missing_columns:
    column_to_fill = missing_columns[0]
    df = fill_with_mode(df, column_to_fill, ['Street Name', 'Block'])

    # Save the DataFrame with the filled column
    df.to_csv('/workspace/concatenated_permits_filled.csv', index=False)
    print(f"Missing values filled for column: {column_to_fill}")

    # Update the list of columns with missing values
    missing_columns.remove(column_to_fill)
    pd.Series(missing_columns).to_csv('/workspace/missing_columns.csv', index=False, header=False)
else:
    print("No more columns with missing values to fill.")
