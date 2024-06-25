import sqlite3
import csv

# Database connection
conn = sqlite3.connect('wwe.db')
cursor = conn.cursor()

# Function to load CSV data into a table
def load_csv_into_table(csv_file_path, table_name, column_mapping=None):
    with open(csv_file_path, 'r') as file:
        reader = csv.DictReader(file)
        columns = [column_mapping.get(field, field) for field in reader.fieldnames] if column_mapping else reader.fieldnames
        placeholders = ', '.join('?' * len(columns))
        insert_query = f'INSERT INTO {table_name} ({", ".join(columns)}) VALUES ({placeholders})'
        
        for row in reader:
            values = [row[original] if original in row and row[original].lower() != 'nan' else None for original in reader.fieldnames]
            if column_mapping:
                # Apply the column mapping to the values
                values = [values[reader.fieldnames.index(original)] for original, new in column_mapping.items() if original in reader.fieldnames]
            # Skip rows with invalid 'id' values for the 'promotions' table
            if table_name == 'promotions' and not values[0].isdigit():
                continue
            try:
                cursor.execute(insert_query, values)
            except sqlite3.IntegrityError as e:
                print(f"Error inserting into {table_name}: {e}")
                print(f"Query: {insert_query}")
                print(f"Values: {values}")
                break  # Stop after the first error to avoid flooding with messages
            except sqlite3.ProgrammingError as e:
                print(f"Programming error: {e}")
                print(f"Query: {insert_query}")
                print(f"Values: {values}")
                break  # Stop after the first error to avoid flooding with messages

# CSV files and corresponding table names with optional column mappings
csv_files = {
    'wrestlers.csv': ('wrestlers', None),
    'belts.csv': ('belts', {'belts_id': 'id', 'belt_name': 'name'}),
    'cards.csv': ('cards', {'card_id': 'id'}),
    'events.csv': ('events', {'event_id': 'id', 'event_name': 'name'}),
    'locations.csv': ('locations', {'location_id': 'id'}),
    'matches.csv': ('matches', None),
    'promotions.csv': ('promotions', None)
}

# Load each CSV file into the corresponding table
for csv_file, (table_name, column_mapping) in csv_files.items():
    load_csv_into_table(csv_file, table_name, column_mapping)

# Commit changes and close the connection
conn.commit()
conn.close()