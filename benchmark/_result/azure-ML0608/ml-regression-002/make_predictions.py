import pandas as pd
import joblib

# Load the trained model
rf = joblib.load('/workspace/electricity_price_predictor.joblib')

# Load the preprocessed test data
test_data = pd.read_csv('/workspace/preprocessed_test_data.csv')

# Predict the 'price actual' using the trained model
test_data['price actual'] = rf.predict(test_data)

# Save the predictions to a CSV file
predictions = test_data[['price actual']]
predictions.to_csv('/workspace/result.csv', index=False)

print("Predictions saved to result.csv.")
