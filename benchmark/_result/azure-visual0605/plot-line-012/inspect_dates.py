import pandas as pd

# Define the column names based on the observation
column_names = ['Date', 'Category', 'RefNo', 'ExtraDate', 'Withdrawal', 'Deposit', 'Balance']

# Load the dataset, skipping the first row and setting the column names
df = pd.read_csv('/workspace/MyTransaction.csv', skiprows=1, names=column_names)

# Print unique date formats
print(df['Date'].unique())
