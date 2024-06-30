import pandas as pd

# Load the dataset
df = pd.read_csv('/workspace/world-data-2023.csv')

# Check for missing values
missing_values = df.isnull().sum()

# Fill missing values with the mean of the column
df_filled = df.fillna(df.mean(numeric_only=True))

# Save the dataframe with missing values filled
df_filled.to_csv('/workspace/world-data-2023-filled.csv', index=False)

# Output the columns with missing values and the number of missing values per column
print(missing_values)
