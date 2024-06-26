import pandas as pd

# Load the partially cleaned DataFrame
df = pd.read_csv('/workspace/Building_Permits.csv', low_memory=False)

# Reset the index to avoid ambiguity between index levels and column labels
df.reset_index(drop=True, inplace=True)

# Function to fill missing values with mode within each group defined by Street Name and Block
def fill_mode(group, column, global_mode):
    mode_value = group.mode()
    if mode_value.size > 0:
        return group.fillna(mode_value.iloc[0])
    else:
        return group.fillna(global_mode)

# Calculate the global mode for the 'zipcode' column
global_mode_zipcode = df['zipcode'].mode().iloc[0] if not df['zipcode'].mode().empty else None

# Fill missing values in the 'zipcode' column using the global mode
df['zipcode'] = df.groupby(['street_name', 'block'])['zipcode'].transform(lambda x: fill_mode(x, 'zipcode', global_mode_zipcode))

# Save the updated DataFrame to a CSV file
df.to_csv('/workspace/Building_Permits.csv', index=False)

# Output the number of missing values for the 'zipcode' column to verify the changes
print(df['zipcode'].isnull().sum())
