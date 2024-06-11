import pandas as pd

# Load the dataset with specified encoding to handle non-UTF-8 characters
df = pd.read_csv('/workspace/OnlineRetail.csv', encoding='ISO-8859-1')

# Display the first few rows of the dataframe and the data types of each column
print(df.head())
print(df.dtypes)
