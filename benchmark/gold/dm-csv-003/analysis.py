import pandas as pd

# Load the data
data = pd.read_csv('../student_data.csv', sep=';')

# Qualification mapping
qualification_mapping = {
    1: 'Secondary Education - 12th Year',
    2: 'Higher Education - Bachelor\'s Degree',
    3: 'Higher Education - Degree',
    4: 'Higher Education - Master\'s',
    5: 'Higher Education - Doctorate',
    6: 'Frequency of Higher Education',
    9: '12th Year of Schooling - Not Completed',
    10: '11th Year of Schooling - Not Completed',
    11: '7th Year (Old)',
    12: 'Other - 11th Year of Schooling',
    14: '10th Year of Schooling',
    18: 'General Commerce Course',
    19: 'Basic Education 3rd Cycle',
    22: 'Technical-Professional Course',
    26: '7th Year of Schooling',
    27: '2nd Cycle of the General High School Course',
    29: '9th Year of Schooling - Not Completed',
    30: '8th Year of Schooling',
    34: 'Unknown',
    35: 'Can\'t Read or Write',
    36: 'Can Read Without 4th Year of Schooling',
    37: 'Basic Education 1st Cycle',
    38: 'Basic Education 2nd Cycle',
    39: 'Technological Specialization Course',
    40: 'Higher Education - Degree (1st Cycle)',
    41: 'Specialized Higher Studies Course',
    42: 'Professional Higher Technical Course',
    43: 'Higher Education - Master (2nd Cycle)',
    44: 'Higher Education - Doctorate (3rd Cycle)'
}

# Extract relevant columns
mothers_qualification = data['Mother\'s qualification'].replace(-1, pd.NA).dropna().map(qualification_mapping)
fathers_qualification = data['Father\'s qualification'].replace(-1, pd.NA).dropna().map(qualification_mapping)

# Calculate frequency of each qualification
mothers_freq = mothers_qualification.value_counts()
fathers_freq = fathers_qualification.value_counts()

# Identify top five qualifications for both mothers and fathers
top_mothers_qualifications = mothers_freq.head(5)
top_fathers_qualifications = fathers_freq.head(5)

# Combine results into a single DataFrame
top_qualifications = pd.DataFrame({
    'Mother\'s Qualification': top_mothers_qualifications.index,
    'Mother\'s Frequency': top_mothers_qualifications.values,
    'Father\'s Qualification': top_fathers_qualifications.index,
    'Father\'s Frequency': top_fathers_qualifications.values
})

# Save the results
top_qualifications.to_csv('top_qualifications.csv', index=False)

print("Analysis completed. Results saved to top_qualifications.csv.")