import pandas as pd

# Load the dataset
df = pd.read_csv('/workspace/scrubbed.csv', low_memory=False)

# Output the unique values in the 'country' column
print(df['country'].unique())
