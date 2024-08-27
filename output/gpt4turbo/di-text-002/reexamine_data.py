import pandas as pd

# Load the CSV file into a DataFrame
df = pd.read_csv('/workspace/world-data-2023.csv')

# Convert 'Agricultural Land( %)' to numeric, setting errors='coerce' to replace non-numeric values with NaN
df['Agricultural Land( %)'] = pd.to_numeric(df['Agricultural Land( %)'], errors='coerce')

# Check the number of non-NaN values in the 'Agricultural Land( %)' column
non_nan_values = df['Agricultural Land( %)'].notna().sum()
print(f"Non-NaN values in 'Agricultural Land( %)': {non_nan_values}")

# If there are non-NaN values, calculate the mean and fill missing values
if non_nan_values > 0:
    # Calculate the mean of the 'Agricultural Land( %)' column, excluding NaN values
    mean_agricultural_land = df['Agricultural Land( %)'].mean()

    # Fill missing values with the mean
    df['Agricultural Land( %)'] = df['Agricultural Land( %)'].fillna(mean_agricultural_land)

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
else:
    result = {
        "highest country": [],
        "Agricultural Land %": []
    }

print(result)
