import pandas as pd

# Load the external dataset
external_dataset = pd.read_csv('/workspace/daigt_external_dataset.csv')

# Display all column names to check for the 'source_text' column
print(external_dataset.columns)

# Display the first few rows of the dataframe including the 'source_text' column if it exists
if 'source_text' in external_dataset.columns:
    print(external_dataset[['id', 'text', 'source_text', 'generated']].head())
else:
    print("The 'source_text' column is not present in the dataframe.")
