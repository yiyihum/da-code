import pandas as pd

# Load the test data
test_data = pd.read_csv('/workspace/test.csv')

# Drop the 'Unnamed: 0' column as it is just an identifier
test_data.drop('Unnamed: 0', axis=1, inplace=True)

# Fill missing values in 'generation_name' with a placeholder
test_data['generation_name'].fillna('Unknown', inplace=True)

# Encode categorical variables using one-hot encoding
test_data_encoded = pd.get_dummies(test_data, columns=['mark', 'model', 'generation_name', 'fuel', 'city', 'province'])

# Save the preprocessed data to a new CSV file for later use
test_data_encoded.to_csv('/workspace/preprocessed_test.csv', index=False)

print("Preprocessing complete. Encoded data saved to /workspace/preprocessed_test.csv")
