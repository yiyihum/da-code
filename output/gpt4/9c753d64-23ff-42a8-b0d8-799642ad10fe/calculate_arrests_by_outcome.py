import pandas as pd

# Load the data
data = pd.read_csv('/workspace/RI-clean.csv')

# Group by 'stop_outcome' and calculate the arrest rates
arrest_rates = data.groupby('stop_outcome')['is_arrested'].value_counts(normalize=True).unstack().fillna(0)

# Save the results to 'result.csv'
arrest_rates.to_csv('/workspace/result.csv')
