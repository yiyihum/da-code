import pandas as pd

# Load the dataset
df = pd.read_csv('/workspace/Books_df.csv')

# Function to calculate IQR and bounds
def calculate_iqr_bounds(data):
    q1 = data.quantile(0.25)
    q3 = data.quantile(0.75)
    iqr = q3 - q1
    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr
    return lower_bound, upper_bound

# Calculate IQR and bounds for 'Price'
price_lower_bound, price_upper_bound = calculate_iqr_bounds(df['Price'])

# Calculate IQR and bounds for 'No. of People rated'
ratings_lower_bound, ratings_upper_bound = calculate_iqr_bounds(df['No. of People Rated'])

# Count outliers for 'Price'
price_outliers_count = df[(df['Price'] < price_lower_bound) | (df['Price'] > price_upper_bound)].shape[0]

# Count outliers for 'No. of People Rated'
ratings_outliers_count = df[(df['No. of People Rated'] < ratings_lower_bound) | (df['No. of People Rated'] > ratings_upper_bound)].shape[0]

# Prepare the results
results = {
    'Metric': ['Price', 'No. of People Rated'],
    'Lower Bound': [price_lower_bound, ratings_lower_bound],
    'Upper Bound': [price_upper_bound, ratings_upper_bound],
    'Outliers Count': [price_outliers_count, ratings_outliers_count]
}

# Convert results to DataFrame
results_df = pd.DataFrame(results)

# Save the results to a CSV file
results_df.to_csv('/workspace/result.csv', index=False)
