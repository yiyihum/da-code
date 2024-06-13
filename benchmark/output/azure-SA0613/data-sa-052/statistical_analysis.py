import pandas as pd
import scipy.stats as stats
from statsmodels.stats.multitest import multipletests

# Load the dataset
energy_b = pd.read_csv('energy_design_b.csv')

# Define the regions and fuel sources based on the template
regions = ['North', 'South', 'East']
fuel_sources = ['Natural_Gas', 'Biofuel', 'Coal']

# Prepare a dictionary to hold the P-values for each comparison
p_values = {}

# Perform ANOVA for each region and fuel source pair
for region in regions:
    data = energy_b[energy_b['Geographical_Region'] == region]
    for i in range(len(fuel_sources)):
        for j in range(i+1, len(fuel_sources)):
            source1 = fuel_sources[i]
            source2 = fuel_sources[j]
            comparison_key = f"{region}: {source1} vs {source2}"
            group1 = data[data['Fuel_Source'] == source1]['CO2_Emissions']
            group2 = data[data['Fuel_Source'] == source2]['CO2_Emissions']
            # Perform the ANOVA (using an independent t-test here for simplicity)
            t_stat, p_val = stats.ttest_ind(group1, group2, equal_var=False)
            p_values[comparison_key] = p_val

# Apply Bonferroni correction
comparisons = list(p_values.keys())
correction_factor = len(comparisons)
corrected_p_values = {key: val * correction_factor for key, val in p_values.items()}

# Write the corrected P-values to the CSV file
with open('bonferroni_corrected_p_values.csv', 'w') as file:
    file.write('Comparison,Bonferroni_Corrected_P_Value\n')
    for comparison in comparisons:
        file.write(f"{comparison},{corrected_p_values[comparison]:.6f}\n")

print("Bonferroni corrected P-values have been calculated and written to 'bonferroni_corrected_p_values.csv'.")
