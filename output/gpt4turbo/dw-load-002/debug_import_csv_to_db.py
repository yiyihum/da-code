import sqlite3
import csv

# Database connection
conn = sqlite3.connect('wwe.db')
cursor = conn.cursor()

# Function to load CSV data into a table
def load_csv_into_table(csv_file_path, table_name):
    with open(csv_file_path, 'r') as file:
        reader = csv.DictReader(file)
        columns = reader.fieldnames
        placeholders = ', '.join('?' * len(columns))
        insert_query = f'INSERT INTO {table_name} ({", ".join(columns)}) VALUES ({placeholders})'
        
        for row in reader:
            values = [row[column] for column in columns]
            try:
                cursor.execute(insert_query, values)
            except sqlite3.IntegrityError as e:
                print(f"Error inserting into {table_name}: {e}")
                print(f"Query: {insert_query}")
                print(f"Values: {values}")
                break  # Stop after the first error to avoid flooding with messages

# CSV files and corresponding table names
csv_files = {
    'wrestlers.csv': 'wrestlers',
    'belts.csv': 'belts',
    'cards.csv': 'cards',
    'events.csv': 'events',
    'locations.csv': 'locations',
    'matches.csv': 'matches',
    'promotions.csv': 'promotions'
}

# Load each CSV file into the corresponding table
for csv_file, table_name in csv_files.items():
    load_csv_into_table(csv_file, table_name)

# Commit changes and close the connection
conn.commit()
conn.close()
