import pandas as pd

# Load the dataset
df = pd.read_csv('/workspace/online_retail_II.csv')

# Display basic information about the dataset
print(df.info())
print(df.head())

# Check for missing values
print(df.isnull().sum())

# Since Customer ID is important for customer segmentation, we will drop rows with missing Customer IDs
df_cleaned = df.dropna(subset=['Customer ID'])

# Convert InvoiceDate to datetime and extract relevant time features if needed
df_cleaned['InvoiceDate'] = pd.to_datetime(df_cleaned['InvoiceDate'])

# Aggregate data by Customer ID to create features for clustering
customer_data = df_cleaned.groupby('Customer ID').agg({
    'Quantity': 'sum',  # Total quantity of products purchased
    'Price': 'mean',    # Average price per unit
    'InvoiceDate': ['min', 'max']  # First and last purchase dates
}).reset_index()

# Flatten the column headers
customer_data.columns = ['_'.join(col).strip() for col in customer_data.columns.values]

# Display the processed customer data
print(customer_data.head())
