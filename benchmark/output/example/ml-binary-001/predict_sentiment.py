import pandas as pd

# Load the test dataset
test_df = pd.read_csv('/workspace/test.csv')

# Assuming 'Output' column represents sentiment with 'Yes' as Positive and 'No' as Negative
test_df['result'] = test_df['Output'].map({'Yes': 'Positive', 'No': 'Negative'})

# Select only the 'result' column as per the result.csv template
result_df = test_df[['result']]

# Save the predictions to result.csv
result_df.to_csv('/workspace/result.csv', index=False)
