import sqlite3
import csv

# Connect to the SQLite database
conn = sqlite3.connect('wwe.db')
cursor = conn.cursor()

# Function to import CSV data into a table
def import_csv_to_table(csv_file_path, table_name, columns):
    with open(csv_file_path, 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        insert_stmt = f'INSERT INTO {table_name} ({", ".join(columns)}) VALUES ({", ".join(["?"] * len(columns))})'
        for row in csv_reader:
            try:
                values = [row[col] if col != 'id' else int(row[col]) for col in columns]
                cursor.execute(insert_stmt, values)
            except ValueError as e:
                print(f"Skipping row with invalid data in {table_name}: {row} - Error: {e}")

# Define the CSV files and their corresponding tables and columns
csv_tables = {
    'belts.csv': ('belts', ['id', 'name']),
    'cards.csv': ('cards', ['id', 'table_id', 'location_id', 'promotion_id', 'event_date', 'event_id', 'url', 'info_html', 'match_html']),
    'events.csv': ('events', ['id', 'name']),
    'locations.csv': ('locations', ['id', 'name']),
    'matches.csv': ('matches', ['id', 'card_id', 'winner_id', 'win_type', 'loser_id', 'match_type_id', 'duration', 'title_id', 'title_change']),
    'promotions.csv': ('promotions', ['id', 'name'])
}

# Import data for each table
for csv_file, (table_name, columns) in csv_tables.items():
    import_csv_to_table(csv_file, table_name, columns)

# Commit changes and close the connection
conn.commit()
conn.close()
