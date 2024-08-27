import pandas as pd

# Load the CSV file into a DataFrame
df = pd.read_csv('/workspace/world-data-2023.csv')

# Convert 'Agricultural Land( %)' to numeric, setting errors='coerce' to replace non-numeric values with NaN
df['Agricultural Land( %)'] = pd.to_numeric(df['Agricultural Land( %)'], errors='coerce')

# Calculate the mean of the 'Agricultural Land( %)' column, excluding NaN values
mean_agricultural_land = df['Agricultural Land( %)'].mean()

# Fill missing values with the mean
df['Agricultural Land( %)'] = df['Agricultural Land( %)'].fillna(mean_agricultural_land)

# Verify that there are no more missing values
missing_values_after = df['Agricultural Land( %)'].isnull().sum()
print(f"Missing values after filling: {missing_values_after}")

# Ensure there is at least one non-NaN value before using idxmax()
if df['Agricultural Land( %)'].notna().any():
    # Find the country with the highest percentage of agricultural land
    highest_country = df.loc[df['Agricultural Land( %)'].idxmax()]['Country']
    highest_value = df['Agricultural Land( %)'].max()
else:
    highest_country = None
    highest_value = None

# Output the result in JSON format
result = {
    "highest country": [highest_country] if highest_country is not None else [],
    "Agricultural Land %": [highest_value] if highest_value is not None else []
}

print(result)
