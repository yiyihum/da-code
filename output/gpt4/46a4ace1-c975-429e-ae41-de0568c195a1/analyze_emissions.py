import pandas as pd
from scipy.stats import f_oneway

# Load the data
data = pd.read_csv('energy_design_b.csv')

# Identify the region and fuel source with the highest CO2 emissions
max_emissions = data.groupby(['Geographical_Region', 'Fuel_Source'])['CO2_Emissions'].sum().idxmax()

# Prepare the data for ANOVA by creating a dictionary where keys are regions and values are lists of emissions for each fuel source
anova_data = {}
for region in data['Geographical_Region'].unique():
    anova_data[region] = {fuel: list(group['CO2_Emissions']) for fuel, group in data[data['Geographical_Region'] == region].groupby('Fuel_Source')}

# Perform ANOVA for each region and collect results
anova_results = []
for region, emissions_dict in anova_data.items():
    # Filter out fuel sources with only one observation
    groups = [emissions for emissions in emissions_dict.values() if len(emissions) > 1]
    if len(groups) > 1:
        # Perform ANOVA
        f_stat, p_value = f_oneway(*groups)
        anova_results.append([region, f_stat, p_value])

# Save the results to a CSV file
anova_results_df = pd.DataFrame(anova_results, columns=['Region', 'F-Statistic', 'P-Value'])
anova_results_df.to_csv('anova_results.csv', index=False)

# Output the region and fuel source with the highest CO2 emissions
print(max_emissions)
