import pandas as pd

# Load the dataset with 'ISO-8859-1' encoding
file_path = 'Year 2009-2010.csv'
data = pd.read_csv(file_path, encoding='ISO-8859-1')

# Display all column names
print(data.columns.tolist())
