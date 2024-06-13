import pandas as pd

# Load the data from the CSV file
df = pd.read_csv('input_without_answer.csv')

# Find the problem with the specified ID
problem = df[df['id'] == '82e2a0']

# Check if the problem was found and print it
if not problem.empty:
    print(problem.iloc[0]['problem'])
else:
    print("Problem with ID '82e2a0' not found.")
