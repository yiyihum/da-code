import pandas as pd

# Load the dataset
df = pd.read_csv('/workspace/online_retail_II.csv')

# Print the column names to verify their exact spelling
print(df.columns.tolist())
