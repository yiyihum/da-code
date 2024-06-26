import sqlite3
import csv

# Connect to the SQLite database
conn = sqlite3.connect('wwe.db')
cursor = conn.cursor()

# Path to the CSV file
csv_file_path = 'wrestlers.csv'

# Open the CSV file and read its contents
with open(csv_file_path, 'r') as csv_file:
    csv_reader = csv.DictReader(csv_file)  # Using DictReader to handle columns by name

    # Prepare the SQL statement for inserting data
    insert_stmt = 'INSERT INTO wrestlers (id, name) VALUES (?, ?)'

    # Insert each row into the wrestlers table
    for row in csv_reader:
        try:
            # Attempt to convert id to integer and insert the row into the database
            wrestler_id = int(row['id'])
            cursor.execute(insert_stmt, (wrestler_id, row['name']))
        except ValueError:
            # Skip rows with invalid integer values for 'id'
            print(f"Skipping row with invalid id: {row['id']}")

# Commit changes and close the connection
conn.commit()
conn.close()
