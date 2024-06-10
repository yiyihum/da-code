import pandas as pd

# Load the dataset
df = pd.read_csv('/workspace/scrubbed.csv')

# Filter the dataset for the specified countries
countries = ['USA', 'Canada', 'United Kingdom', 'Australia', 'Germany']
sightings_count = {}

for country in countries:
    # Assuming the country column is named 'country' in the dataset
    sightings_count[country] = df[df['country'] == country].shape[0]

# Output the count of sightings for each country
print(sightings_count)
