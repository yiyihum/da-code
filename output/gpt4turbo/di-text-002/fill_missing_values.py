import pandas as pd

# Load the CSV file into a DataFrame
df = pd.read_csv('/workspace/world-data-2023.csv')

# Check for missing values in the 'Agricultural Land( %)' column
missing_values = df['Agricultural Land( %)'].isnull().sum()
print(f"Missing values in 'Agricultural Land( %)': {missing_values}")

# Calculate the mean of the 'Agricultural Land( %)' column, excluding NaN values
mean_agricultural_land = df['Agricultural Land( %)'].mean()

# Fill missing values with the mean
df['Agricultural Land( %)'].fillna(mean_agricultural_land, inplace=True)

# Verify that there are no more missing values
missing_values_after = df['Agricultural Land( %)'].isnull().sum()
print(f"Missing values after filling: {missing_values_after}")

# Find the country with the highest percentage of agricultural land
highest_country = df.loc[df['Agricultural Land( %)'].idxmax()]['Country']
highest_value = df['Agricultural Land( %)'].max()

# Output the result in JSON format
result = {
    "highest country": [highest_country],
    "Agricultural Land %": [highest_value]
}

print(result)
