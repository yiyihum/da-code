import pandas as pd

# Load the data
df = pd.read_csv('students.csv')

# Filter for international students
international_students = df[df['inter_dom'] == 'Inter'].copy()

# Convert 'dep' column to numeric, setting errors='coerce' to convert non-numeric values to NaN
international_students.loc[:, 'dep'] = pd.to_numeric(international_students['dep'], errors='coerce')

# Check if there are any non-NaN values in the 'dep' column
non_nan_count = international_students['dep'].notna().sum()

# Output the count of non-NaN values in the 'dep' column
print(f"Count of non-NaN values in 'dep' column: {non_nan_count}")
