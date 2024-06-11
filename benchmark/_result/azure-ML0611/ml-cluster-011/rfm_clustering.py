import pandas as pd
from sklearn.cluster import KMeans
from datetime import datetime

# Load the preprocessed dataset
df = pd.read_csv('/workspace/OnlineRetail.csv', encoding='ISO-8859-1')
df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'], format='%d-%m-%Y %H:%M')
df['TotalPrice'] = df['Quantity'] * df['UnitPrice']
df = df.dropna(subset=['CustomerID'])
df['CustomerID'] = df['CustomerID'].astype(int)

# RFM Analysis
# Recency: Days since last purchase
current_date = df['InvoiceDate'].max() + pd.Timedelta(days=1)
df['Recency'] = (current_date - df.groupby('CustomerID')['InvoiceDate'].transform('max')).dt.days

# Frequency: Number of purchases
df['Frequency'] = df.groupby('CustomerID')['InvoiceNo'].transform('nunique')

# Monetary: Total amount of money spent
df['Monetary'] = df.groupby('CustomerID')['TotalPrice'].transform('sum')

# Prepare RFM dataframe for clustering
rfm_df = df.groupby('CustomerID').agg({
    'Recency': 'min',
    'Frequency': 'max',
    'Monetary': 'sum'
}).reset_index()

# Select the number of clusters
kmeans = KMeans(n_clusters=4, random_state=42)
rfm_df['Cluster'] = kmeans.fit_predict(rfm_df[['Recency', 'Frequency', 'Monetary']])

# Save the clustering results to a CSV file
rfm_df.to_csv('/workspace/cluster.csv', index=False)

# Check the first few rows of the clustering result
print(rfm_df.head())
