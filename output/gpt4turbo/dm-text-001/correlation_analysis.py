import pandas as pd
import json

# Load the dataset
df = pd.read_csv('world-data-2023.csv')

# Replace newline characters in column names
df.columns = df.columns.str.replace('\n', ' ', regex=False)

# Convert 'Density (P/Km2)' to numeric, coercing errors to NaN
df['Density (P/Km2)'] = pd.to_numeric(df['Density (P/Km2)'], errors='coerce')

# Replace missing values with the mean for the relevant columns
df['Density (P/Km2)'].fillna(df['Density (P/Km2)'].mean(), inplace=True)
df['Life expectancy'].fillna(df['Life expectancy'].mean(), inplace=True)

# Remove dollar signs, commas, and spaces from the GDP column and convert it to float
df['GDP'] = df['GDP'].replace({'\$': '', ',': '', ' ': ''}, regex=True).astype(float)

# Calculate the correlation coefficients
correlation_density_life_expectancy = df['Density (P/Km2)'].corr(df['Life expectancy'])
correlation_density_gdp = df['Density (P/Km2)'].corr(df['GDP'])

# Output the results in JSON format
output = {
    "Correlation between Population Density and Life Expectancy": [correlation_density_life_expectancy],
    "Correlation between Population Density and GDP": [correlation_density_gdp]
}

# Save the output to a JSON file
output_file = 'correlation_results.json'
with open(output_file, 'w') as file:
    json.dump(output, file)

print(output)
