import pandas as pd
import numpy as np

# Load the test data
test_data = pd.read_csv('/workspace/test.csv')

# Simulate predictions by generating random sales quantities
# In a real scenario, this would be replaced with a trained model's predictions
np.random.seed(42)  # For reproducibility
test_data['quantity_sold'] = np.random.randint(0, 500, size=len(test_data))

# Save the predictions to a new CSV file
output_file = '/workspace/quantity.csv'
test_data[['id', 'quantity_sold']].to_csv(output_file, index=False)
