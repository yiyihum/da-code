import pandas as pd

# Load the dataset
df = pd.read_csv('/workspace/Books_df.csv')

# Convert 'Price' and 'No. of People rated' to numeric, coercing errors to NaN
df['Price'] = pd.to_numeric(df['Price'], errors='coerce')
df['No. of People rated'] = pd.to_numeric(df['No. of People rated'], errors='coerce')

# Drop rows with NaN values in these columns
df = df.dropna(subset=['Price', 'No. of People rated'])

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

# Print the calculated values for debugging
print(f"Price Lower Bound: {price_lower_bound}, Upper Bound: {price_upper_bound}, IQR: {price_iqr}, Outliers: {price_outliers_count}")
print(f"Ratings Lower Bound: {ratings_lower_bound}, Upper Bound: {ratings_upper_bound}, IQR: {ratings_iqr}, Outliers: {ratings_outliers_count}")

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
