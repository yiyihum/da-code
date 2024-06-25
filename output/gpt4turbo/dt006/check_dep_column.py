import pandas as pd

# Load the data from the CSV file
df = pd.read_csv('students.csv')

# Print unique values in the 'dep' column
unique_dep_values = df['dep'].unique()
print("Unique values in 'dep' column:", unique_dep_values)
