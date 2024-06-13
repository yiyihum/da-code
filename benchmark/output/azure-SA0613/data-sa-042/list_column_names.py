import pandas as pd

# Load the dataset
df = pd.read_csv('/workspace/Books_df.csv')

# Print the column names
print(df.columns.tolist())
