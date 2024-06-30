import pandas as pd

# List of CSV files to merge
csv_files = ['RI-clean_1.csv', 'RI-clean_2.csv', 'RI-clean_3.csv', 'RI-clean_4.csv', 'RI-clean_5.csv']

# Read and concatenate all CSV files into one DataFrame
df = pd.concat((pd.read_csv(f) for f in csv_files), ignore_index=True)

# Save the concatenated DataFrame to 'RI-clean.csv'
df.to_csv('RI-clean.csv', index=False)
