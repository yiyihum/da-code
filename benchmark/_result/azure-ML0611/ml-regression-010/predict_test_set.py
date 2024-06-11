import pandas as pd

# Load the test data
test_data = pd.read_csv('/workspace/drugsComTest_raw.csv')

# Preprocess the test data similarly to the training data
test_data['condition'].fillna('Unknown', inplace=True)

# Select the 'rating' feature from the test data for prediction
X_test = test_data[['rating']]

# Use the trained regressor to predict the 'usefulCount' (usefulness) on the test data
test_data['usefulness'] = regressor.predict(X_test)

# Create the 'Usefulness.csv' file with only the 'usefulness' column
test_data[['usefulness']].to_csv('/workspace/Usefulness.csv', index=False)
