import pandas as pd

# Load the data for men's and women's results
men_results = pd.read_csv('men_results.csv')
women_results = pd.read_csv('women_results.csv')

# Display the first few rows of each dataframe to understand their structure
print("Men's results:")
print(men_results.head())
print("\nWomen's results:")
print(women_results.head())
