import pandas as pd

# Load the compressed CSV file to inspect its contents
file_path = 'closing_odds.csv.gz'
df = pd.read_csv(file_path, compression='gzip')

# Display the first few rows of the DataFrame
print(df.head())
