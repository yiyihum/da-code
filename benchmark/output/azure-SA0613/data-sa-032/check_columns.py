import pandas as pd

# Load the dataset
df = pd.read_csv('crisis_portfolio.csv')

# Print the columns of the DataFrame
print(df.columns.tolist())
