import pandas as pd

# Load the train.csv file into a DataFrame
df = pd.read_csv('train.csv')

# Exclude the 'Sex' column
df = df.drop(columns=['Sex'])

# Calculate the correlation matrix
corr_matrix = df.corr()

# Print the correlation matrix
print(corr_matrix)
