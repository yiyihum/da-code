import pandas as pd
import re

# Load the resumes data
df = pd.read_csv('/workspace/resumes.csv')

# Define patterns to extract job titles, technical skills, and educational degrees
job_title_pattern = r'([A-Z][A-Za-z\s]+)\s+Summary'
technical_skills_pattern = r'(Technical Skills|Skills|TECHNICAL SKILLS|SKILLS)[^\n]+'
education_pattern = r'(Bachelor|Master|B\.Sc\.|M\.Sc\.|B\.A\.|M\.A\.|PhD|Bachelors|Masters|Doctorate|Degree in)[^\n]+'

# Function to extract information based on a pattern
def extract_info(pattern, text):
    match = re.search(pattern, text)
    return match.group() if match else None

# Apply the extraction function to the 'Resume_str' column
df['Job_Title'] = df['Resume_str'].apply(lambda x: extract_info(job_title_pattern, x))
df['Technical_Skills'] = df['Resume_str'].apply(lambda x: extract_info(technical_skills_pattern, x))
df['Education'] = df['Resume_str'].apply(lambda x: extract_info(education_pattern, x))

# Filter out rows with any missing values in the new columns
df_filtered = df.dropna(subset=['Job_Title', 'Technical_Skills', 'Education'])

# Save the result to a new CSV file
df_filtered.to_csv('/workspace/result.csv', index=False)
