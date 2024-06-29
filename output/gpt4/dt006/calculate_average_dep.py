import pandas as pd

# Load the data
df = pd.read_csv('students.csv')

# Filter for international students
international_students = df[df['inter_dom'] == 'Inter'].copy()

# Convert 'dep' column to numeric, setting errors='coerce' to convert non-numeric values to NaN
international_students.loc[:, 'dep'] = pd.to_numeric(international_students['dep'], errors='coerce')

# Filter out rows where 'dep' is NaN
international_students_with_dep = international_students[international_students['dep'].notna()]

# Calculate the count and average depression score for students with a valid 'dep' score
summary = {
    'International Students Count': international_students_with_dep.shape[0],
    'Average Depression Score': international_students_with_dep['dep'].mean(skipna=True)
}

# Convert summary to DataFrame
summary_df = pd.DataFrame([summary])

# Save the result to 'result.csv'
summary_df.to_csv('result.csv', index=False)
