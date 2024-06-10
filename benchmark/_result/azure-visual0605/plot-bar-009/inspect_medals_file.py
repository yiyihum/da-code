import pandas as pd

# Load the Medals data to inspect its structure
medals_df = pd.read_excel('/workspace/Medals.xlsx')

# Print the first few rows of the dataframe to understand its structure
print(medals_df.head())
