import pandas as pd
import joblib

# Load the test data
test_data = pd.read_csv('/workspace/test.csv')

# Drop the columns that were not used during model training
columns_to_drop = ['forecast wind offshore eday ahead', 'generation hydro pumped storage aggregated']
test_features = test_data.drop(columns=columns_to_drop + ['time'])

# Load the trained model
model = joblib.load('/workspace/electricity_price_model.joblib')

# Predict the electricity prices on the test dataset
test_data['price actual'] = model.predict(test_features)

# Save the predictions to a CSV file
test_data[['time', 'price actual']].to_csv('/workspace/result.csv', index=False)

print("Predictions made and saved to result.csv.")
