import pandas as pd

# Load the CSV file into a DataFrame
df = pd.read_csv('input_without_answer.csv')

# Retrieve the problem with the specified ID
problem_id = "430b63"
problem = df[df['id'] == problem_id]['problem'].iloc[0]

# Output the problem to verify its content
print(problem)
