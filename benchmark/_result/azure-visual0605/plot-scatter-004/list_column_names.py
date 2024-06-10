import pandas as pd

# Load the dataset
df = pd.read_csv('/workspace/appstore_games.csv')

# Print all column names to identify the ones we need
print(df.columns.tolist())
