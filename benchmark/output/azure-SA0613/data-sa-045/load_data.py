import pandas as pd

# Load the datasets for 1975 and 2012
df_1975 = pd.read_csv('finch_beaks_1975.csv')
df_2012 = pd.read_csv('finch_beaks_2012.csv')

# Output the first few rows of each dataframe to verify the data
print(df_1975.head())
print(df_2012.head())
