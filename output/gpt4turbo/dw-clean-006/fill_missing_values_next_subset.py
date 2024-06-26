import pandas as pd

# Load the partially cleaned DataFrame
df = pd.read_csv('/workspace/Building_Permits_partial.csv', low_memory=False)

# Reset the index to avoid ambiguity between index levels and column labels
df.reset_index(drop=True, inplace=True)

# Function to fill missing values with mode within each group defined by Street Name and Block
def fill_mode(group, column, global_mode):
    if group[column].isnull().sum() > 0:
        mode_value = group[column].mode()
        if not mode_value.empty:
            group[column] = group[column].fillna(mode_value.iloc[0])
        else:
            group[column] = group[column].fillna(global_mode)
    return group

# Identify columns with missing values
columns_with_missing_values = df.columns[df.isnull().any()].tolist()

# Continue with the next subset of columns with missing values to avoid timeouts
# Adjust the range as needed based on the previous subset processed
next_subset_columns = columns_with_missing_values[5:10]  # Adjust the range as needed

# Fill missing values for the next subset of columns
for column in next_subset_columns:
    # Calculate the global mode to use if the group mode is empty
    global_mode = df[column].mode().iloc[0] if not df[column].mode().empty else None
    # Apply the fill_mode function to each group
    df[column] = df.groupby(['street_name', 'block'])[column].transform(lambda x: fill_mode(x, column, global_mode))
    # Infer object types to avoid FutureWarning about downcasting
    df[column] = df[column].infer_objects()

# Save the updated partially cleaned DataFrame to a CSV file
df.to_csv('/workspace/Building_Permits_partial.csv', index=False)

# Output the number of missing values for the next subset of columns to verify the changes
print(df[next_subset_columns].isnull().sum())
