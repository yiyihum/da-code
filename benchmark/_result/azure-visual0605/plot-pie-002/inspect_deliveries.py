import pandas as pd

# Load the deliveries dataset
deliveries = pd.read_csv('deliveries.csv')

# Display the first few rows of the dataframe to inspect the columns
print(deliveries.head())
