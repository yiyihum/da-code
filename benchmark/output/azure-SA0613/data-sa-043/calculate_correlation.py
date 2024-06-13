import pandas as pd

# Load the dataset
df = pd.read_csv('/workspace/airlines_reviews.csv')

# Select the relevant columns for correlation
columns_of_interest = ['Overall Rating', 'Seat Comfort', 'Staff Service', 'Food & Beverages']
df = df[columns_of_interest]

# Calculate the correlation matrix
correlation_matrix = df.corr()

# Save the correlation matrix to a CSV file
correlation_matrix.to_csv('/workspace/result.csv')
