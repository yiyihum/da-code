import pandas as pd

# Load the dataset
df = pd.read_csv('/workspace/online_retail_II.csv')

# Clean the data by dropping rows with missing Customer IDs
df_cleaned = df.dropna(subset=['Customer ID'])

# Convert InvoiceDate to datetime
df_cleaned.loc[:, 'InvoiceDate'] = pd.to_datetime(df_cleaned['InvoiceDate'])

# Aggregate data by Customer ID
customer_data = df_cleaned.groupby('Customer ID').agg({
    'Quantity': 'sum',  # Total quantity of products purchased
    'Price': 'mean',    # Average price per unit
    'InvoiceDate': ['min', 'max']  # First and last purchase dates
}).reset_index()

# Flatten the column headers
customer_data.columns = ['_'.join(col).strip() for col in customer_data.columns.values]

# Save the preprocessed customer data to a CSV file
customer_data.to_csv('/workspace/customer_data.csv', index=False)

print("Preprocessed customer data saved to customer_data.csv")
