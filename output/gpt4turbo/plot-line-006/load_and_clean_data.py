import pandas as pd

# Load the dataset
df = pd.read_csv('/workspace/GlobalTemperatures.csv')

# Convert the 'dt' column to datetime
df['dt'] = pd.to_datetime(df['dt'])

# Filter out the rows where the country is in the excluded list
excluded_countries = [
    'Denmark', 'Antarctica', 'France', 'Europe', 'Netherlands',
    'United Kingdom', 'Africa', 'South America'
]

# Since the dataset does not contain a country column, we will assume that
# the exclusion of countries will be handled in a later step if necessary.

# Standardize country names by removing "(Europe)"
# This step is not applicable here as there is no country column in this dataset.

# Check the first few rows of the dataframe to ensure it's loaded correctly
print(df.head())
