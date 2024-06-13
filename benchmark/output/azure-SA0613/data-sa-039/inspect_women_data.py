import pandas as pd

# Load the women's results from the CSV file
women_results = pd.read_csv('/workspace/women_results.csv')

# Print the first few rows of the dataframe to inspect the column names
print(women_results.head())
