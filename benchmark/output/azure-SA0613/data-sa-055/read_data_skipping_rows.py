import pandas as pd

# Attempt to read the CSV file, skipping initial rows that are not part of the data
try:
    # Skip rows that are not part of the actual data (assuming the first few lines are comments)
    df = pd.read_csv('frog_tongue.csv', comment='#')
    print(df.head())
except pd.errors.ParserError as e:
    print("ParserError after skipping comments:", e)
