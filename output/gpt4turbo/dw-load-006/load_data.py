import csv
import sqlite3

# Define the database filename
db_filename = 'database.db'

# Establish a connection to the database
conn = sqlite3.connect(db_filename)
cursor = conn.cursor()

# Function to create a table and import data from a CSV file
def import_csv_to_table(csv_filename, table_name):
    # Open the CSV file
    with open(csv_filename, 'r') as csv_file:
        # Read the CSV file
        csv_reader = csv.reader(csv_file)
        # Extract the headers
        headers = next(csv_reader)
        # Create the table with appropriate column names
        cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} ({', '.join('[' + column + ']' for column in headers)})")
        # Insert the data into the table
        for row in csv_reader:
            placeholders = ', '.join('?' * len(row))
            cursor.execute(f"INSERT INTO {table_name} VALUES ({placeholders})", row)

# List of CSV files and corresponding table names
csv_files = [
    ('company.csv', 'company'),
    ('ev311.csv', 'ev311'),
    ('fortune.csv', 'fortune'),
    ('stackexchange.csv', 'stackexchange')
]

# Import each CSV file into the database
for csv_file, table_name in csv_files:
    import_csv_to_table(csv_file, table_name)

# Commit changes and close the connection
conn.commit()
conn.close()
