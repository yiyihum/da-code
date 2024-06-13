import pandas as pd

# Load the dataset
df = pd.read_csv('input_without_answer.csv')

# Retrieve the problem with ID '246d26'
problem = df[df['id'] == '246d26']

# Check if the problem exists and print it
if not problem.empty:
    print(problem.iloc[0]['problem'])
else:
    print("Problem with ID '246d26' not found.")
