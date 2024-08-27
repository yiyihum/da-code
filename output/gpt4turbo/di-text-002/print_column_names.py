import pandas as pd

# Load the CSV file into a DataFrame
df = pd.read_csv('/workspace/world-data-2023.csv')

# Print the column names to identify the agricultural land percentage column
print(df.columns.tolist())
