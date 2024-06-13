import pandas as pd

# Load the men's results from the Excel file
men_results = pd.read_excel('/workspace/men_results.xls')

# Print the first few rows of the dataframe to inspect the column names
print(men_results.head())
