import pandas as pd
import json

# Load the dataset
df = pd.read_csv('/workspace/bestsellers with categories.csv')

# Define a function to calculate the outlier ranges
def calculate_outlier_ranges(data):
    q1 = data.quantile(0.25)
    q3 = data.quantile(0.75)
    iqr = q3 - q1
    outlier_range = [q1 - 1.5 * iqr, q3 + 1.5 * iqr]
    extreme_outlier_range = [q1 - 3 * iqr, q3 + 3 * iqr]
    return outlier_range, extreme_outlier_range

# Assuming the review counts are in a column named 'Reviews'
review_counts = df['Reviews']
outlier_range, extreme_outlier_range = calculate_outlier_ranges(review_counts)

# Output the results in JSON format
output = {
    "Outlier's range": outlier_range,
    "Extreme Outlier's range": extreme_outlier_range
}

# Save the output to a JSON file
output_file = '/workspace/outliers.json'
with open(output_file, 'w') as f:
    json.dump(output, f)

print("Outlier and extreme outlier ranges calculated and saved to outliers.json")
