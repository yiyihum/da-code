import sqlite3
import csv

# Connect to the SQLite database
conn = sqlite3.connect('wwe.db')
cursor = conn.cursor()

# Function to import CSV data into a table
def import_csv_to_table(csv_file_path, table_name, column_mappings):
    with open(csv_file_path, 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        columns = column_mappings.keys()
        db_columns = column_mappings.values()
        insert_stmt = f'INSERT INTO {table_name} ({", ".join(db_columns)}) VALUES ({", ".join(["?"] * len(columns))})'
        for row in csv_reader:
            try:
                values = [row[csv_col] if csv_col != 'id' else int(row[csv_col]) for csv_col in columns]
                cursor.execute(insert_stmt, values)
            except ValueError as e:
                print(f"Skipping row with invalid data in {table_name}: {row} - Error: {e}")

# Define the CSV files and their corresponding tables and column mappings
csv_tables = {
    'belts.csv': ('belts', {'belts_id': 'id', 'belt_name': 'name'}),
    'cards.csv': ('cards', {'card_id': 'id', 'table_id': 'table_id', 'location_id': 'location_id', 'promotion_id': 'promotion_id', 'event_date': 'event_date', 'event_id': 'event_id', 'url': 'url', 'info_html': 'info_html', 'match_html': 'match_html'}),
    'events.csv': ('events', {'event_id': 'id', 'event_name': 'name'}),
    'locations.csv': ('locations', {'location_id': 'id', 'name': 'name'}),
    'matches.csv': ('matches', {'id': 'id', 'card_id': 'card_id', 'winner_id': 'winner_id', 'win_type': 'win_type', 'loser_id': 'loser_id', 'match_type_id': 'match_type_id', 'duration': 'duration', 'title_id': 'title_id', 'title_change': 'title_change'}),
    'promotions.csv': ('promotions', {'id': 'id', 'name': 'name'})
}

# Import data for each table
for csv_file, (table_name, column_mappings) in csv_tables.items():
    import_csv_to_table(csv_file, table_name, column_mappings)

# Commit changes and close the connection
conn.commit()
conn.close()
