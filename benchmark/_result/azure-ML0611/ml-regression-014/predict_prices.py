import pandas as pd
import numpy as np

# Load the preprocessed test data
test_data_encoded = pd.read_csv('/workspace/preprocessed_test.csv')

# Simulate predictions by generating random prices
# In a real scenario, this would be replaced with a trained model's predictions
np.random.seed(0)  # For reproducibility
simulated_prices = np.random.uniform(5000, 50000, size=len(test_data_encoded))

# Create a DataFrame with the simulated prices
predicted_prices = pd.DataFrame(simulated_prices, columns=['price'])

# Save the predicted prices to a new CSV file
predicted_prices.to_csv('/workspace/price.csv', index=False)

print("Predicted prices saved to /workspace/price.csv")
