import pandas as pd

# Load the data from the CSV file
data = pd.read_csv('Kaggle7-1_0\\marketing_data.csv')

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
selected_columns = ['Teenhome', 'MntWines', 'MntFruits', 'MntMeatProducts', 'MntFishProducts', 'MntSweetProducts', 'MntGoldProds']
data_selected = data[selected_columns]

# Filter the data to include only households with teenagers
data_with_teens = data_selected[data_selected['Teenhome'] > 0]

# Calculate the sum of purchases for each product category among these households
sum_purchases_with_teens = data_with_teens.drop(columns=['Teenhome']).sum().to_frame(name='TotalPurchases')

# Rename the column names to corresponding product categories
sum_purchases_with_teens.rename(index=product_mapping, inplace=True)

# Save the results to a CSV file
sum_purchases_with_teens.to_csv('Kaggle7-1_0\\gold\\problem.csv')

print("Results saved to problem.csv.")