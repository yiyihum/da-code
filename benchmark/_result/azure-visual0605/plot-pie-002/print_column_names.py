import pandas as pd

# Load the deliveries dataset
deliveries = pd.read_csv('deliveries.csv')

# Print the column names to identify the correct one for the batsman's name
print(deliveries.columns.tolist())
