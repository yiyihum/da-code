import pandas as pd

# Load the data from the CSV file
data = pd.read_csv('Kaggle7-1\\marketing_data.csv')

# Create a dictionary to map the product categories
product_mapping = {
    'MntWines': 'Wine',
    'MntFruits': 'Fruits',
    'MntMeatProducts': 'Meat Products',
    'MntFishProducts': 'Fish Products',
    'MntSweetProducts': 'Sweet Products',
    'MntGoldProds': 'Gold Products'
}

# Select the relevant columns for analysis
selected_columns = ['Kidhome', 'MntWines', 'MntFruits', 'MntMeatProducts', 'MntFishProducts', 'MntSweetProducts', 'MntGoldProds']
data_selected = data[selected_columns]

# Group the data by 'Kidhome' and calculate the sum of purchases for each product category
grouped_data = data_selected.groupby('Kidhome').sum()

# Rename the column names to corresponding product categories
grouped_data.rename(columns=product_mapping, inplace=True)

# Save the results to a CSV file
grouped_data.to_csv('Kaggle7-1\\gold\\result.csv')

print("Results saved to result.csv.")