import pandas as pd

# Load the data
df = pd.read_csv('students.csv')

# Display unique values in the 'dep' column
unique_dep_values = df['dep'].unique()

# Output the unique values of the 'dep' column
print(f"Unique values in 'dep' column: {unique_dep_values}")
