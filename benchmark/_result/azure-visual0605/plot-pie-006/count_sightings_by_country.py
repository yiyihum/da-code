import pandas as pd

# Load the dataset
df = pd.read_csv('/workspace/scrubbed.csv', low_memory=False)

# Define the country codes for the specified countries
country_codes = {'USA': 'us', 'Canada': 'ca', 'United Kingdom': 'gb', 'Australia': 'au', 'Germany': 'de'}
sightings_count = {}

for country, code in country_codes.items():
    sightings_count[country] = df[df['country'] == code].shape[0]

# Output the count of sightings for each country
print(sightings_count)
