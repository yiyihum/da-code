import pandas as pd
from datetime import datetime

# Load the dataset
df = pd.read_csv('/workspace/bank_transactions.csv')

# Convert CustomerDOB and TransactionDate to datetime objects
df['CustomerDOB'] = pd.to_datetime(df['CustomerDOB'], format='%d/%m/%y', errors='coerce')
df['TransactionDate'] = pd.to_datetime(df['TransactionDate'], format='%d/%m/%y', errors='coerce')

# Calculate age of the customers
current_date = datetime.now()
df['Age'] = df['CustomerDOB'].apply(lambda dob: (current_date - dob).days // 365 if pd.notnull(dob) else None)

# Encode the CustGender column
df['CustGender'] = df['CustGender'].map({'F': 0, 'M': 1})

# Drop columns that won't be used for clustering
df.drop(['TransactionID', 'CustomerID', 'CustomerDOB', 'CustLocation', 'TransactionDate', 'TransactionTime'], axis=1, inplace=True)

# Display the first few rows of the preprocessed dataframe
print(df.head())
