import pandas as pd
from datetime import datetime

# Function to calculate age from DOB
def calculate_age(dob, current_date):
    try:
        # This will create a 2000s date for a year that is obviously meant to be in the 1900s
        if dob.year > current_date.year:
            dob = dob.replace(year=dob.year - 100)
        return (current_date - dob).days // 365
    except:
        return None

# Load the dataset
df = pd.read_csv('/workspace/bank_transactions.csv')

# Convert CustomerDOB to datetime objects, fixing the century issue
df['CustomerDOB'] = pd.to_datetime(df['CustomerDOB'], format='%d/%m/%y', errors='coerce')

# Calculate the current date
current_date = datetime.now()

# Calculate age of the customers
df['Age'] = df['CustomerDOB'].apply(lambda dob: calculate_age(dob, current_date))

# Encode the CustGender column
df['CustGender'] = df['CustGender'].map({'F': 0, 'M': 1})

# Drop columns that won't be used for clustering
df.drop(['TransactionID', 'CustomerID', 'CustomerDOB', 'CustLocation', 'TransactionDate', 'TransactionTime'], axis=1, inplace=True)

# Handle missing or incorrect age values by dropping or imputing
df = df[df['Age'] > 0]

# Display the first few rows of the preprocessed dataframe
print(df.head())
