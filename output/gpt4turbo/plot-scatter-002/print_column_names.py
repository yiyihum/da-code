import pandas as pd

# Load the compressed CSV file to inspect its contents
file_path = 'closing_odds.csv.gz'
df = pd.read_csv(file_path, compression='gzip')

# Print the column names of the DataFrame
print(df.columns.tolist())
