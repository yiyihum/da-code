import pandas as pd

# Load the data from the CSV file
df = pd.read_csv('students.csv')

# Convert 'dep' column to numeric, coercing errors to NaN
df['dep'] = pd.to_numeric(df['dep'], errors='coerce')

# Filter the data for international students
international_students = df[df['inter_dom'] == 'Inter']

# Calculate the number of international students
num_international_students = international_students.shape[0]

# Calculate the average depression score for international students, ignoring NaN values
average_depression_score = international_students['dep'].mean()

# Output the results
summary = {
    'Number of International Students': num_international_students,
    'Average Depression Score': average_depression_score
}

# Print the summary
print(summary)
