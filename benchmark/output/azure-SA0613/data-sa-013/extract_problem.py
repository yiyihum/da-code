import csv

# Define the ID of the problem we are looking for
problem_id = "5277ed"

# Open the CSV file and read the contents
with open('input_without_answer.csv', mode='r') as csvfile:
    # Create a CSV reader
    csvreader = csv.DictReader(csvfile)
    
    # Initialize a variable to store the problem
    problem = None
    
    # Loop through the rows in the CSV
    for row in csvreader:
        # Check if the current row has the problem ID we are looking for
        if row['id'] == problem_id:
            problem = row['problem']
            break

# Output the problem to a text file
with open('problem.txt', 'w') as problem_file:
    problem_file.write(problem if problem else 'Problem not found.')
