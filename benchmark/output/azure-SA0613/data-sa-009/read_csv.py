import pandas as pd

# Load the CSV file into a DataFrame
df = pd.read_csv('input_without_answer.csv')

# Find the problem with the specified ID
problem = df[df['id'] == '8ee6f3']

# Check if the problem was found and print it
if not problem.empty:
    print(problem.iloc[0]['problem'])
else:
    print("Problem with ID '8ee6f3' not found.")
