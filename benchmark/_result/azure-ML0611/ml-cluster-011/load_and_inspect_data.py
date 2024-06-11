import pandas as pd

# Load the dataset
df = pd.read_csv('/workspace/OnlineRetail.csv')

# Display the first few rows of the dataframe and the data types of each column
print(df.head())
print(df.dtypes)
