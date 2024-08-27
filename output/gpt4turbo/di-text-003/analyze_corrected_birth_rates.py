import pandas as pd
import json

# Load the data
df = pd.read_csv('/workspace/world-data-2023.csv')

# Check for missing values in the 'Birth Rate' column
missing_birth_rates = df['Birth Rate'].isnull().sum()

# If there are missing values, fill them with the mean birth rate
if missing_birth_rates > 0:
    mean_birth_rate = df['Birth Rate'].mean()
    df['Birth Rate'].fillna(mean_birth_rate, inplace=True)

# Identify the top 5 countries with the highest birth rates
top_5_high = df.nlargest(5, 'Birth Rate')['Country'].tolist()

# Identify the top 5 countries with the lowest birth rates
top_5_low = df.nsmallest(5, 'Birth Rate')['Country'].tolist()

# Output the results in JSON format
result = {
    "Top 5 countries with High Birth Rate": top_5_high,
    "Top 5 countries with Lowest Birth Rate": top_5_low
}

# Save the result to a JSON file
result_file = '/workspace/birth_rates_result.json'
with open(result_file, 'w') as f:
    json.dump(result, f)

print(result)
