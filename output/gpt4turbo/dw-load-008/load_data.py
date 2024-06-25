import sqlite3
import csv

# Create a new SQLite database
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Function to create a table and import CSV data into it
def import_csv_to_table(csv_file, table_name):
    # Create table based on the CSV header
    with open(csv_file, 'r') as file:
        reader = csv.reader(file)
        header = next(reader)
        columns = ', '.join([f'"{column}" TEXT' for column in header])
        cursor.execute(f'CREATE TABLE IF NOT EXISTS {table_name} ({columns})')
    
    # Import data into the table
    with open(csv_file, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header row
        for row in reader:
            placeholders = ', '.join('?' * len(row))
            cursor.execute(f'INSERT INTO {table_name} VALUES ({placeholders})', row)

# List of CSV files and corresponding table names
csv_files = {
    'athletes.csv': 'athletes',
    'countries.csv': 'countries',
    'country_stats.csv': 'country_stats',
    'summer.csv': 'summer_games',
    'winter_games.csv': 'winter_games'
}

# Import each CSV file into the database
for csv_file, table_name in csv_files.items():
    import_csv_to_table(csv_file, table_name)

# Commit changes and close the connection
conn.commit()
conn.close()
