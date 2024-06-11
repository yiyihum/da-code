import pandas as pd
import numpy as np

# Load the test data
test_data = pd.read_csv('/workspace/test.csv')

# Preprocessing: Fill missing values with appropriate values or assumptions
test_data['Accidents or damage'].fillna('None Reported', inplace=True)
test_data['Clean title'].fillna('Yes', inplace=True)
test_data['1-owner vehicle'].fillna('Yes', inplace=True)
test_data['Personal use only'].fillna('Yes', inplace=True)

# Define a function to determine the status of the car
def determine_status(row):
    if row['Accidents or damage'] == 'None Reported' and row['Clean title'] == 'Yes' and        row['1-owner vehicle'] == 'Yes' and row['Personal use only'] == 'Yes':
        return 'new'
    else:
        return 'used'

# Apply the function to create a new column 'new&used'
test_data['new&used'] = test_data.apply(determine_status, axis=1)

# Save the results to a CSV file
result_path = '/workspace/result.csv'
test_data[['name', 'new&used']].to_csv(result_path, index=False)

print(f"Results saved to {result_path}")
