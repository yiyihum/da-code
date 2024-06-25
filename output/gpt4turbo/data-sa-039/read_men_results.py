import pandas as pd

# Load the Excel file
men_results_path = 'men_results.xls'
men_results = pd.read_excel(men_results_path)

# Display the first few rows to understand the structure
print(men_results.head())
