import pandas as pd

# Load the data from the CSV file
df = pd.read_csv('students.csv')

# Convert 'dep' column to numeric, coercing errors to NaN
df['dep'] = pd.to_numeric(df['dep'], errors='coerce')

# Filter the data for international students
international_students = df[df['inter_dom'] == 'Inter']

# Print unique 'dep' values for international students
unique_international_dep_values = international_students['dep'].unique()
print("Unique 'dep' values for international students:", unique_international_dep_values)
