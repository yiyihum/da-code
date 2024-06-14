import pandas as pd

# Load the men's results from the Excel file
men_results = pd.read_excel('/workspace/men_results.xls')

# Filter the men's results for matches since 2002
men_results_since_2002 = men_results[men_results['Year'] >= 2002]

# Save the filtered men's results to a CSV file
men_results_since_2002.to_csv('/workspace/men_results_since_2002.csv', index=False)

# Load the women's results from the CSV file
women_results = pd.read_csv('/workspace/women_results.csv')

# Filter the women's results for matches since 2002
women_results_since_2002 = women_results[women_results['Year'] >= 2002]

# Save the filtered women's results to a CSV file
women_results_since_2002.to_csv('/workspace/women_results_since_2002.csv', index=False)