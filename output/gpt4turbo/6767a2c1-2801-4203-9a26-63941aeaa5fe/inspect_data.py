import pandas as pd

# Load the dataset
file_path = 'Year 2009-2010.csv'
data = pd.read_csv(file_path)

# Display the first few rows of the dataframe
print(data.head())
