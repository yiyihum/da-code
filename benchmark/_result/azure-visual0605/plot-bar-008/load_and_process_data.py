import pandas as pd

# Load the dataset
df = pd.read_csv('/workspace/multipleChoiceResponses.csv', low_memory=False)

# Filter out rows that do not clearly specify a country
df = df[df['Q3'].notnull() & (df['Q3'] != 'Other')]

# Replace long country names with abbreviations
country_replacements = {
    'United States of America': 'USA',
    'United Kingdom of Great Britain and Northern Ireland': 'UK & Northern Ireland'
}
df['Q3'].replace(country_replacements, inplace=True)

# Replace 'Prefer not to say' and 'Prefer to self-describe' with 'Others'
gender_replacements = {
    'Prefer not to say': 'Others',
    'Prefer to self-describe': 'Others'
}
df['Q1'].replace(gender_replacements, inplace=True)

# Filter for the specified countries
countries = [
    'USA', 'UK & Northern Ireland', 'India', 'China', 'Russia',
    'Brazil', 'Germany', 'France', 'Canada', 'Japan'
]
df_filtered = df[df['Q3'].isin(countries)]

# Save the processed data to a new CSV file
df_filtered.to_csv('/workspace/processed_survey_data.csv', index=False)
