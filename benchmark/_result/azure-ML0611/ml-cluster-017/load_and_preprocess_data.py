import pandas as pd
from datetime import datetime

# Load the data
df = pd.read_csv('/workspace/bank_transactions.csv')

# Convert 'CustomerDOB' to age
current_year = datetime.now().year
df['CustomerDOB'] = pd.to_datetime(df['CustomerDOB'], errors='coerce', format='%d/%m/%y')
df['CustomerDOB'] = df['CustomerDOB'].apply(lambda x: current_year - x.year if pd.notnull(x) else x)

# Rename 'CustomerDOB' to 'CustomerAge'
df.rename(columns={'CustomerDOB': 'CustomerAge'}, inplace=True)

# Encode 'CustGender' as binary variable
df['CustGender'] = df['CustGender'].map({'F': 0, 'M': 1})

# Normalize 'CustAccountBalance' and 'TransactionAmount (INR)'
df['CustAccountBalance'] = (df['CustAccountBalance'] - df['CustAccountBalance'].mean()) / df['CustAccountBalance'].std()
df['TransactionAmount (INR)'] = (df['TransactionAmount (INR)'] - df['TransactionAmount (INR)'].mean()) / df['TransactionAmount (INR)'].std()

# Drop unnecessary columns for clustering
df.drop(['TransactionID', 'CustomerID', 'CustLocation', 'TransactionDate', 'TransactionTime'], axis=1, inplace=True)

# Save the processed data to a new CSV file for further analysis
processed_file_path = '/workspace/processed_bank_transactions.csv'
df.to_csv(processed_file_path, index=False)

processed_file_path
