import csv

# Function to find the sum of the unique increasing geometric sequence
def find_geometric_sequence_sum():
    # The first term (a) must be a 2-digit number, and the common ratio (r) must be such that
    # the sequence remains within 2-digit numbers and is increasing.
    for a in range(10, 100):  # 2-digit numbers start from 10
        for r in range(11, 20):  # Common ratio r/10 will be between 1.1 and 1.9
            r = r / 10
            # Generate the sequence
            sequence = [a * (r ** n) for n in range(5)]
            # Check if all terms are 2-digit integers and the sequence is strictly increasing
            if all(10 <= term < 100 and term == int(term) for term in sequence):
                # Since the problem states the sequence is unique, we return the sum
                return int(sum(sequence))
    return None

# Calculate the sum of the sequence
sequence_sum = find_geometric_sequence_sum()

# Write the result to the result.csv file
with open('result.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['id', 'answer'])
    writer.writerow(['5277ed', sequence_sum])

# Output the result to verify
print(f"The sum of the unique increasing geometric sequence is: {sequence_sum}")
