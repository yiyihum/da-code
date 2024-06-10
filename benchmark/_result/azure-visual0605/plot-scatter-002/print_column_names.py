import pandas as pd

# Read the compressed CSV file
df = pd.read_csv('/workspace/odds_series_matches.csv.gz', compression='gzip', encoding='latin1')

# Trim whitespace from column names
df.columns = df.columns.str.strip()

# Print the column names to identify the correct ones for average odds
print(df.columns.tolist())
