import pandas as pd

# Load the external dataset
external_dataset = pd.read_csv('/workspace/daigt_external_dataset.csv')

# Display the first few rows of the dataframe
print(external_dataset.head())

# Display the structure of the dataframe
print(external_dataset.info())
