import sqlite3
import csv

# Connect to the SQLite database
conn = sqlite3.connect('wwe.db')
cursor = conn.cursor()

# Path to the CSV file
csv_file_path = 'wrestlers.csv'

# Open the CSV file and read its contents
with open(csv_file_path, 'r') as csv_file:
    csv_reader = csv.reader(csv_file)
    next(csv_reader)  # Skip the header row

    # Prepare the SQL statement for inserting data
    insert_stmt = 'INSERT INTO wrestlers (id, name) VALUES (?, ?)'

    # Insert each row into the wrestlers table
    for row in csv_reader:
        cursor.execute(insert_stmt, row)

# Commit changes and close the connection
conn.commit()
conn.close()
