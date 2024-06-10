import pandas as pd

# Read the first few rows of the compressed CSV file to inspect the data
df = pd.read_csv('/workspace/odds_series_matches.csv.gz', compression='gzip', encoding='latin1', nrows=5)

# Output the first few rows to understand the data structure
print(df.head())
