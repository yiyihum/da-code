import pandas as pd

# Load the model and the preprocessor
pipeline = pd.read_pickle('simplified_model_pipeline.pkl')

# Load the test data
test_data = pd.read_csv('/workspace/Test.csv')

# Separate features and ID column
X_test = test_data.drop('ID', axis=1)
ids = test_data['ID']

# Preprocess the test data and make predictions
test_predictions = pipeline.predict(X_test)

# Create a DataFrame with the ID and the predictions
results = pd.DataFrame({'ID': ids, 'income_above_limit': test_predictions})

# Convert predictions back to the original labels
results['income_above_limit'] = results['income_above_limit'].apply(lambda x: 'Above limit' if x == 1 else 'Below limit')

# Save the results to a CSV file
results.to_csv('/workspace/results.csv', index=False)
