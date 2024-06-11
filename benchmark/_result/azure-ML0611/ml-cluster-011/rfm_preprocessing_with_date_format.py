import pandas as pd

# Load the dataset with specified encoding
df = pd.read_csv('/workspace/OnlineRetail.csv', encoding='ISO-8859-1')

# Convert 'InvoiceDate' to datetime with the correct format
df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'], format='%d-%m-%Y %H:%M')

# Calculate the total price
df['TotalPrice'] = df['Quantity'] * df['UnitPrice']

# Drop rows with missing CustomerID
df = df.dropna(subset=['CustomerID'])

# Convert 'CustomerID' to int
df['CustomerID'] = df['CustomerID'].astype(int)

# Check the processed dataframe
print(df.head())
print(df.dtypes)
