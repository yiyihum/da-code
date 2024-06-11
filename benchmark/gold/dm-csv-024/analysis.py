import pandas as pd

# Assume the dataset is stored in a file named 'marketing_data.csv'
data = pd.read_csv('Kaggle7-1_3\\marketing_data.csv')

# Remove non-numeric characters from 'Income' column and convert to numeric
data['Income'] = data['Income'].replace('[\$,]', '', regex=True).astype(float)

# Perform missing value imputation for 'Income'
data['Income'] = data.groupby(['Education', 'Marital_Status'])['Income'].transform(lambda x: x.fillna(x.mean()))

# Define the income intervals
income_intervals = [0, 50000, 75000, 100000, 150000, float('inf')]
income_labels = ['(0, 50k]', '(50k, 75k]', '(75k, 100k]', '(100k, 150k]', '(150k, ∞)']

# Create a new column 'Income_Bracket' for income intervals
data['Income_Bracket'] = pd.cut(data['Income'], bins=income_intervals, labels=income_labels)

# Group by 'Income_Bracket' and sum 'NumWebPurchases' and 'NumStorePurchases'
income_purchase_summary = data.groupby('Income_Bracket')[['NumWebPurchases', 'NumStorePurchases']].sum().reset_index()

# Save the grouped data to a CSV file named 'purchase_by_income.csv'
income_purchase_summary.to_csv('purchase_by_income.csv', index=False)