import pandas as pd

# Load the data
data = pd.read_csv('energy_design_b.csv')

# Aggregate CO2 emissions by region and fuel source
aggregated_data = data.groupby(['Geographical_Region', 'Fuel_Source']).agg({'CO2_Emissions': 'sum'}).reset_index()

# Find the region and source with the highest CO2 emissions
max_emissions = aggregated_data.loc[aggregated_data['CO2_Emissions'].idxmax()]

# Output the result
print(max_emissions)
