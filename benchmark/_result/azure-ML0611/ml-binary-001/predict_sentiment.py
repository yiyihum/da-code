import pandas as pd

# Load the test data
test_df = pd.read_csv('/workspace/test.csv')

# Map 'Yes' to 'Positive' and 'No' to 'Negative'
test_df['result'] = test_df['Output'].map({'Yes': 'Positive', 'No': 'Negative'})

# Select only the 'result' column
result_df = test_df[['result']]

# Save the predictions to 'result.csv'
result_df.to_csv('/workspace/result.csv', index=False)
