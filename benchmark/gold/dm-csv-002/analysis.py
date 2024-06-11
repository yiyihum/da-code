import pandas as pd

# Read the student data
df = pd.read_csv('../student_data.csv', sep=';')

# Define the function for mapping marital status
def MS(num):
    if num == 1:
        return 'Never Married'
    else:
        return 'Previously Married'

# Apply the function to the 'Marital status' column
df['Marital Status'] = df['Marital status'].apply(MS)

# Calculate the counts of 'Never Married' and 'Previously Married'
counts = df['Marital Status'].value_counts()

# Create a DataFrame with the counts arranged into two columns
result_df = pd.DataFrame({
    'Never Married': [counts.get('Never Married', 0)],
    'Previously Married': [counts.get('Previously Married', 0)]
})

# Save the resultant DataFrame to a CSV file
result_df.to_csv('../result.csv', index=False)