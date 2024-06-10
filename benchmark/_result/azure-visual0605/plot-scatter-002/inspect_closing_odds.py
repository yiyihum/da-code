import pandas as pd

# Read the first few rows of the 'closing_odds.csv.gz' file to inspect the data
df_closing_odds = pd.read_csv('/workspace/closing_odds.csv.gz', compression='gzip', encoding='latin1', nrows=5)

# Output the column names and the first few rows to understand the data structure
print(df_closing_odds.columns.tolist())
print(df_closing_odds.head())
