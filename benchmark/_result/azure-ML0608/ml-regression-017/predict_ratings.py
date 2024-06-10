import pandas as pd

# Load the test data
test_df = pd.read_csv('/workspace/test.csv')

# Check if 'review_percentage' has missing values
missing_values = test_df['review_percentage'].isnull().sum()
if missing_values > 0:
    # If there are missing values, fill them with the mean of the column
    mean_value = test_df['review_percentage'].mean()
    test_df['review_percentage'] = test_df['review_percentage'].fillna(mean_value)

# Create a new DataFrame with the 'rating' column
ratings_df = test_df[['review_percentage']].rename(columns={'review_percentage': 'rating'})

# Save the ratings to a CSV file
ratings_df.to_csv('/workspace/rating.csv', index=False)
