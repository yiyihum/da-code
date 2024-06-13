import pandas as pd

# Load the data from the CSV file
df = pd.read_csv('input_without_answer.csv')

# Print the first few rows of the dataframe to inspect the column names
print(df.head())
