import pandas as pd

# Load the dataset
file_path = '/workspace/Online Retail.xlsx'
data = pd.read_excel(file_path)

# Display basic information about the dataset
print(data.info())
print(data.head())
