import pandas as pd

# Load the partially cleaned DataFrame
df = pd.read_csv('/workspace/Building_Permits_partial.csv', low_memory=False)

# Reset the index to avoid ambiguity between index levels and column labels
df.reset_index(drop=True, inplace=True)

# Function to fill missing values with mode within each group defined by Street Name and Block
def fill_mode(group, column):
    mode_value = group.mode()
    if mode_value.size > 0:
        return group.fillna(mode_value.iloc[0])
    else:
        return group

# Identify columns with missing values
columns_with_missing_values = df.columns[df.isnull().any()].tolist()

# Continue with the remaining columns with missing values to complete the cleaning process
remaining_columns = columns_with_missing_values[15:]  # Adjust the range to include all remaining columns

# Fill missing values for the remaining columns
for column in remaining_columns:
    # Apply the fill_mode function to each group
    df[column] = df.groupby(['street_name', 'block'])[column].transform(lambda x: fill_mode(x, column))

# Save the fully cleaned DataFrame to a CSV file
df.to_csv('/workspace/Building_Permits.csv', index=False)

# Output the number of missing values for the remaining columns to verify the changes
print(df[remaining_columns].isnull().sum())
