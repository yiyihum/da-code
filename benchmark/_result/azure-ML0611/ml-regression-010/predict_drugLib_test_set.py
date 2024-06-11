import pandas as pd

# Load the test data from the correct file
test_data = pd.read_csv('/workspace/drugLibTest_raw.csv')

# Use the trained regressor to predict the 'usefulCount' (usefulness) on the test data
# Note: The model was trained on the 'rating' feature from the training data
test_data['usefulness'] = regressor.predict(test_data[['rating']])

# Create the 'Usefulness.csv' file with only the 'usefulness' column
test_data[['usefulness']].to_csv('/workspace/Usefulness.csv', index=False)
