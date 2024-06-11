import pandas as pd

# Load the CSV file into a pandas DataFrame
df = pd.read_csv('Kaggle7-1_2\\marketing_data.csv')

# Calculate the sum of accepted offers for each row (customer)
df['TotalAccepted'] = df[['AcceptedCmp1', 'AcceptedCmp2', 'AcceptedCmp3', 'AcceptedCmp4', 'AcceptedCmp5']].sum(axis=1)

# Calculate the average number of accepted offers
average_acceptance = df['TotalAccepted'].mean()

print(f"The average number of offers accepted per customer across all campaigns is: {average_acceptance}")