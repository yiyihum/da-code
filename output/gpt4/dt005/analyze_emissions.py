import pandas as pd

# Load the data
df = pd.read_csv('product_emissions.csv')

# Convert carbon_footprint_pcf to numeric, removing any non-numeric characters
df['carbon_footprint_pcf'] = pd.to_numeric(df['carbon_footprint_pcf'], errors='coerce')

# Find the latest year in the dataset
latest_year = df['year'].max()

# Filter the data for the latest year
latest_data = df[df['year'] == latest_year]

# Group by industry_group and aggregate the data
industry_summary = latest_data.groupby('industry_group').agg(
    companies_count=pd.NamedAgg(column='company', aggfunc=lambda x: x.nunique()),
    total_carbon_footprint=pd.NamedAgg(column='carbon_footprint_pcf', aggfunc='sum')
).reset_index()

# Sort the results by total carbon footprint in descending order
industry_summary_sorted = industry_summary.sort_values(by='total_carbon_footprint', ascending=False)

# Save the results to a CSV file
industry_summary_sorted.to_csv('/workspace/industry_carbon_footprint.csv', index=False)
