import pandas as pd

# Load the data from the CSV file
df = pd.read_csv('students.csv')

# Filter the data for international students
international_students = df[df['inter_dom'] == 'Inter']

# Print unique values in the 'todep' column for international students
unique_todep_values = international_students['todep'].unique()
print("Unique 'todep' values for international students:", unique_todep_values)
