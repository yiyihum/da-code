import pandas as pd

# Read the first few lines of the compressed CSV file to inspect the column headers
df = pd.read_csv('/workspace/odds_series_matches.csv.gz', compression='gzip', encoding='latin1', nrows=5)

# Output the column names to understand the structure of the CSV file
print(df.columns.tolist())
