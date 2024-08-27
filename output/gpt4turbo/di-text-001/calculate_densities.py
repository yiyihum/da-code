import pandas as pd

# Load the dataset with missing values filled
df = pd.read_csv('/workspace/world-data-2023-filled.csv')

# Rename the 'Density\n(P/Km2)' column to 'Density' for easier access
df.rename(columns={'Density\n(P/Km2)': 'Density'}, inplace=True)

# Find the country with the highest population density
highest_density_country = df[df['Density'] == df['Density'].max()]['Country'].tolist()

# Find the country with the lowest population density
lowest_density_country = df[df['Density'] == df['Density'].min()]['Country'].tolist()

# Output the results in JSON format
result = {
    "highest country": highest_density_country,
    "lowest country": lowest_density_country
}

print(result)
