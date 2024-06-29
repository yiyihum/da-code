import pandas as pd
from datetime import datetime

# Load the data
df = pd.read_csv('online12M.csv')

# Convert InvoiceDate to datetime
df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])

# Calculate Total Price
df['TotalPrice'] = df['Quantity'] * df['UnitPrice']

# Calculate Recency, Frequency, Monetary values for each customer
NOW = datetime.now()
rfm_table = df.groupby('CustomerID').agg({
    'InvoiceDate': lambda x: (NOW - x.max()).days,
    'InvoiceNo': lambda x: len(x.unique()),
    'TotalPrice': lambda x: x.sum()
})

# Rename the columns
rfm_table.rename(columns={'InvoiceDate': 'Recency',
                          'InvoiceNo': 'Frequency',
                          'TotalPrice': 'Monetary'}, inplace=True)

# Calculate RFM Score
rfm_table['R_Score'] = pd.qcut(rfm_table['Recency'], 4, labels=['1','2','3','4'])
rfm_table['F_Score'] = pd.qcut(rfm_table['Frequency'].rank(method='first'), 4, labels=['4','3','2','1'])
rfm_table['M_Score'] = pd.qcut(rfm_table['Monetary'], 4, labels=['4','3','2','1'])

# Combine RFM scores into a single score
rfm_table['RFM_Score'] = rfm_table['R_Score'].astype(str) + rfm_table['F_Score'].astype(str) + rfm_table['M_Score'].astype(str)

# Define RFM levels
segt_map = {
    r'[1-2][1-2]': 'High Value',
    r'[1-2][3-4]': 'Medium Value',
    r'[3-4][1-2]': 'Low Value',
    r'[3-4][3-4]': 'Lost'
}

# Assign a segment to each customer
rfm_table['Segment'] = rfm_table['RFM_Score']
rfm_table['Segment'] = rfm_table['Segment'].replace(segt_map, regex=True)

# Save the result to a CSV file
rfm_table.to_csv('result.csv')
