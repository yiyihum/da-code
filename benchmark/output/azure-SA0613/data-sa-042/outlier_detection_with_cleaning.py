import pandas as pd

# Load the dataset
df = pd.read_csv('/workspace/Books_df.csv')

# Clean the 'Price' column by removing the currency symbol and commas
df['Price'] = df['Price'].str.replace('₹', '').str.replace(',', '').astype(float)

# The 'No. of People rated' column is already in a numeric format, so no cleaning is needed

# Function to calculate IQR and bounds
def calculate_iqr_bounds(data):
    q1 = data.quantile(0.25)
    q3 = data.quantile(0.75)
    iqr = q3 - q1
    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr
    return lower_bound, upper_bound, iqr

# Calculate IQR and bounds for 'Price'
price_lower_bound, price_upper_bound, price_iqr = calculate_iqr_bounds(df['Price'])

# Calculate IQR and bounds for 'No. of People rated'
ratings_lower_bound, ratings_upper_bound, ratings_iqr = calculate_iqr_bounds(df['No. of People rated'])

# Count outliers for 'Price'
price_outliers_count = df[(df['Price'] < price_lower_bound) | (df['Price'] > price_upper_bound)].shape[0]

# Count outliers for 'No. of People rated'
ratings_outliers_count = df[(df['No. of People rated'] < ratings_lower_bound) | (df['No. of People rated'] > ratings_upper_bound)].shape[0]

# Prepare the results
results = {
    'Metric': ['Price', 'No. of People rated'],
    'Lower Bound': [price_lower_bound, ratings_lower_bound],
    'Upper Bound': [price_upper_bound, ratings_upper_bound],
    'IQR': [price_iqr, ratings_iqr],
    'Outliers Count': [price_outliers_count, ratings_outliers_count]
}

# Convert results to DataFrame
results_df = pd.DataFrame(results)

# Save the results to a CSV file
results_df.to_csv('/workspace/result.csv', index=False)
