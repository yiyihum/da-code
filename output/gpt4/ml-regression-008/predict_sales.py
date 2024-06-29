import pandas as pd

# Load the test data
test_data = pd.read_csv('/workspace/test.csv')

# Since we do not have a model or training data, we will use a simple heuristic for demonstration.
# For instance, we can assume that the quantity sold is inversely proportional to the price.
# This is a naive assumption and should not be used for actual predictions.
test_data['quantity_sold'] = 1000 - test_data['price'] / 1000

# Ensure that the quantity_sold is non-negative
test_data['quantity_sold'] = test_data['quantity_sold'].clip(lower=0)

# Save the predictions to a CSV file
test_data[['quantity_sold']].to_csv('/workspace/quantity.csv', index=False)
