import pandas as pd

# Load the dataset
df = pd.read_csv('airlines_reviews.csv')

# Select the relevant columns for correlation
columns_of_interest = ['Overall Rating', 'Seat Comfort', 'Staff Service', 'Food & Beverages']
df_subset = df[columns_of_interest]

# Calculate the correlation matrix
correlation_matrix = df_subset.corr()

# Save the correlation matrix to 'result.csv', following the format of 'sample_result.csv'
correlation_matrix.to_csv('result.csv')
