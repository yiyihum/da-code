import pandas as pd

# Load the property data
property_data = pd.read_csv('/workspace/property.csv')

# Display basic information about the dataset
print(property_data.info())

# Display the first few rows of the dataset
print(property_data.head())
