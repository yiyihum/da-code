import pandas as pd

# Load the data for men's and women's results
men_data = pd.read_csv('men_results.csv')
women_data = pd.read_csv('women_results.csv')

# Display the first few rows of each dataframe to understand their structure
print("Men's data sample:")
print(men_data.head())

print("\nWomen's data sample:")
print(women_data.head())
