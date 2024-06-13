import pandas as pd
import scipy.stats as stats

# Load the data
data = pd.read_csv('energy_design_b.csv')

# Get the unique geographical regions and fuel sources
regions = data['Geographical_Region'].unique()
fuel_sources = data['Fuel_Source'].unique()

# Prepare a dictionary to hold ANOVA results
anova_results = {
    'Geographical_Region': [],
    'F-Value': [],
    'P-Value': []
}

# Perform ANOVA for each region
for region in regions:
    # Filter data for the current region
    region_data = data[data['Geographical_Region'] == region]
    
    # Prepare a list to hold emissions data for each fuel source
    emissions_by_source = []
    
    for source in fuel_sources:
        # Filter data for the current fuel source
        source_data = region_data[region_data['Fuel_Source'] == source]['CO2_Emissions']
        emissions_by_source.append(source_data)
    
    # Perform ANOVA test
    f_val, p_val = stats.f_oneway(*emissions_by_source)
    
    # Append results to the dictionary
    anova_results['Geographical_Region'].append(region)
    anova_results['F-Value'].append(f_val)
    anova_results['P-Value'].append(p_val)

# Convert the results dictionary to a DataFrame
anova_results_df = pd.DataFrame(anova_results)

# Save the ANOVA results to a CSV file
anova_results_df.to_csv('anova_results.csv', index=False)
