import pandas as pd
from sklearn.cluster import KMeans
from datetime import datetime

# Load the dataset with ISO-8859-1 encoding
df = pd.read_csv('/workspace/OnlineRetail.csv', encoding='ISO-8859-1')

# Convert InvoiceDate from string to datetime
df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'], format='%d-%m-%Y %H:%M')

# Calculate Recency, Frequency, Monetary values
# Recency: Days since last purchase
# Frequency: Number of transactions
# Monetary: Total amount spent

# Get the most recent purchase date to calculate recency
snapshot_date = df['InvoiceDate'].max() + pd.Timedelta(days=1)

# Aggregate data by CustomerID
rfm_df = df.groupby('CustomerID').agg({
    'InvoiceDate': lambda x: (snapshot_date - x.max()).days,
    'InvoiceNo': 'nunique',
    'Quantity': 'sum',
    'UnitPrice': 'sum'
}).rename(columns={
    'InvoiceDate': 'Recency',
    'InvoiceNo': 'Frequency',
    'Quantity': 'MonetaryQuantity',
    'UnitPrice': 'MonetaryPrice'
})

# Calculate Monetary value as Quantity * UnitPrice
rfm_df['Monetary'] = rfm_df['MonetaryQuantity'] * rfm_df['MonetaryPrice']

# Drop intermediate Monetary columns
rfm_df.drop(columns=['MonetaryQuantity', 'MonetaryPrice'], inplace=True)

# Normalize the RFM data
rfm_normalized = (rfm_df - rfm_df.mean()) / rfm_df.std()

# Choose an arbitrary number of clusters for KMeans
kmeans = KMeans(n_clusters=5, random_state=1)

# Fit the model
rfm_normalized['Cluster'] = kmeans.fit_predict(rfm_normalized[['Recency', 'Frequency', 'Monetary']])

# Prepare the dataframe with the original RFM values and the cluster labels
rfm_normalized['Recency'] = rfm_df['Recency']
rfm_normalized['Frequency'] = rfm_df['Frequency']
rfm_normalized['Monetary'] = rfm_df['Monetary']

# Save the clustering results
rfm_normalized.to_csv('/workspace/cluster.csv', columns=['Recency', 'Frequency', 'Monetary', 'Cluster'], index=True, header=['Feature_1', 'Feature_2', 'Feature_3', 'Cluster'])
