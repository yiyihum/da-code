import pandas as pd

# Load the intermediate DataFrame
df = pd.read_csv('/workspace/Building_Permits_intermediate.csv', low_memory=False)

# Reset the index to avoid ambiguity between index levels and column labels
df.reset_index(drop=True, inplace=True)

# Function to fill missing values with mode within each group defined by Street Name and Block
def fill_mode(group, column):
    if group[column].isnull().sum() > 0:
        mode_value = group[column].mode()
        if not mode_value.empty:
            group[column] = group[column].fillna(mode_value.iloc[0])
    return group

# Identify columns with missing values
columns_with_missing_values = df.columns[df.isnull().any()].tolist()

# Fill missing values for each column one by one
for column in columns_with_missing_values:
    # Apply the fill_mode function to each group
    df[column] = df.groupby(['street_name', 'block'])[column].transform(lambda x: x.fillna(x.mode().iloc[0] if not x.mode().empty else x))

# Save the cleaned DataFrame to a CSV file
df.to_csv('/workspace/Building_Permits.csv', index=False)

# Output the number of missing values for each column to verify the changes
print(df.isnull().sum())