import pandas as pd

def infer_status(row):
    # Simple heuristic to infer the status:
    # If the car has mileage less than a certain threshold, no reported accidents or damage,
    # has a clean title, is a 1-owner vehicle, and is for personal use only, it's considered new.
    # Otherwise, it's considered used.
    if (row['Mileage'] < 1000 and row['Accidents or damage'] == 'None Reported' and
        row['Clean title'] == 'Yes' and row['1-owner vehicle'] == 'Yes' and
        row['Personal use only'] == 'Yes'):
        return 'New'
    else:
        return 'Used'

# Load the test data
test_data = pd.read_csv('/workspace/test.csv')

# Infer the status for each car
test_data['new&used'] = test_data.apply(infer_status, axis=1)

# Save the results to a CSV file
result_file = '/workspace/result.csv'
test_data[['name', 'new&used']].to_csv(result_file, index=False)
