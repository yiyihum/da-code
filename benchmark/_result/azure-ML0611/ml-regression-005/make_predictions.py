import pandas as pd

# Load the trained model
model = pd.read_pickle('/workspace/car_price_model.pkl')

# Load the test data
test_data = pd.read_csv('/workspace/test.csv')

# Preprocess the test data and predict prices
predicted_prices = model.predict(test_data)

# Create a DataFrame with the predicted prices
predictions = pd.DataFrame(predicted_prices, columns=['price'])

# Save the predictions to a CSV file
predictions.to_csv('/workspace/price.csv', index=False)

print("Predictions saved to price.csv.")
