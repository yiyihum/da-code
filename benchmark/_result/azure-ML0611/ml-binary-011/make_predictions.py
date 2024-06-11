import pandas as pd

# Load the test data
test_data = pd.read_csv('/workspace/Test.csv')

# Select the same subset of features as used for training
features = ['age', 'education', 'wage_per_hour']
X_test = test_data[features]

# Use the trained pipeline to make predictions on the test data
predictions = pipeline.predict(X_test)

# Create a DataFrame with the ID and the predicted income_above_limit
results = pd.DataFrame({
    'ID': test_data['ID'],
    'income_above_limit': predictions
})

# Convert the numerical predictions back to the original categorical labels
results['income_above_limit'] = results['income_above_limit'].apply(lambda x: 'Above limit' if x == 1 else 'Below limit')

# Write the results to a CSV file
results.to_csv('/workspace/results.csv', index=False)
