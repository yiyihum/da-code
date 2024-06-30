import pandas as pd

# Load the parking violation data
df = pd.read_csv('/workspace/parking_violation.csv')

# Assuming that a combination of 'Plate ID', 'Violation Code', 'Issue Date', and 'Violation Time'
# can uniquely identify a violation, we will look for duplicates based on these columns.
duplicate_columns = ['Plate ID', 'Violation Code', 'Issue Date', 'Violation Time']

# Find duplicate rows based on the specified columns
duplicates = df[df.duplicated(subset=duplicate_columns, keep=False)]

# Sort the duplicates by 'Plate ID' and 'Issue Date' to review them more easily
duplicates_sorted = duplicates.sort_values(by=['Plate ID', 'Issue Date'])

# Save the duplicates to a CSV file for further analysis
duplicates_sorted.to_csv('/workspace/duplicate_violations.csv', index=False)

# Print the number of duplicate records found
print(f"Number of duplicate records found: {duplicates_sorted.shape[0]}")
