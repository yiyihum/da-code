import pandas as pd

# Load the test dataset
test_df = pd.read_csv('/workspace/test.csv')

# Create a unique identifier 'id' by concatenating 'week', 'center_id', and 'meal_id'
test_df['id'] = test_df['week'].astype(str) + '_' + test_df['center_id'].astype(str) + '_' + test_df['meal_id'].astype(str)

# Since we don't have a trained model or training data, we will use a simple heuristic for prediction.
# For the purpose of this task, let's assume the number of orders is the average of checkout_price and base_price.
# This is just a placeholder and not a valid prediction method.
test_df['num_orders'] = (test_df['checkout_price'] + test_df['base_price']) / 2

# Prepare the submission dataframe
submission_df = test_df[['id', 'num_orders']]

# Write the submission dataframe to a CSV file
submission_df.to_csv('/workspace/submission.csv', index=False)
