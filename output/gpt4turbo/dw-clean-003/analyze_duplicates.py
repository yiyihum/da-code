import pandas as pd

# Load the parking violation data
df = pd.read_csv('/workspace/parking_violation.csv')

# Display the first few rows of the dataframe to understand its structure
print(df.head())
