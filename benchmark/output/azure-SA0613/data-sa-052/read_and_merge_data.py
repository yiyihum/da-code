import pandas as pd

# Load the datasets
energy_a = pd.read_csv('energy_design_a.csv')
energy_b = pd.read_csv('energy_design_b.csv')

# Since the 'energy_design_a.csv' does not contain geographical regions, we need to find a way to merge or relate it with 'energy_design_b.csv'.
# Let's print out the unique values in the 'Fuel_Source' and 'Building_Type' columns from 'energy_design_a.csv'
# and the unique values in the 'Geographical_Region' and 'Fuel_Source' columns from 'energy_design_b.csv'
# to understand how to relate these datasets.

print("Unique values in energy_design_a.csv:")
print("Fuel_Source:", energy_a['Fuel_Source'].unique())
print("Building_Type:", energy_a['Building_Type'].unique())

print("\nUnique values in energy_design_b.csv:")
print("Geographical_Region:", energy_b['Geographical_Region'].unique())
print("Fuel_Source:", energy_b['Fuel_Source'].unique())
