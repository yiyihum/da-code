import pandas as pd

# Load the combined data
df = pd.read_csv('/workspace/combined_data.csv')

# Display basic information about the DataFrame
print(df.info())

# Display summary statistics for numerical columns
print(df.describe())

# Check for the number of missing values in each column
print(df.isnull().sum())

# Check for the number of unique customers
print(df['Customer ID'].nunique())

# Check for the number of cancellation transactions
cancellations = df[df['Invoice'].str.contains('C', na=False)]
print(f"Number of cancellation transactions: {len(cancellations)}")
