import pandas as pd

# Load the test data
test_df = pd.read_csv('/workspace/test.csv')

# Create mock predictions (this is just for demonstration and does not reflect real model predictions)
mock_predictions = ['business'] * len(test_df)

# Add the mock predictions to the dataframe
test_df['CATEGORY'] = mock_predictions

# Save the mock predictions to a CSV file
test_df[['CATEGORY']].to_csv('/workspace/category.csv', index=False)
