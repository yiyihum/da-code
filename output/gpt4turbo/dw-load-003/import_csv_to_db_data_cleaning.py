import sqlite3
import csv
from datetime import datetime

# Connect to the sport.db database
conn = sqlite3.connect('sport.db')
cursor = conn.cursor()

# A dictionary mapping CSV file names to their corresponding table names and columns
csv_to_table = {
    'country_info.csv': ('Country', ['id', 'name']),
    'league_info.csv': ('League', ['id', 'country_id', 'name']),
    'match.csv': ('Match', None),  # Assuming 'match.csv' has the correct headers
    'player.csv': ('Player', ['height', 'id', 'birthday', 'player_fifa_api_id', 'player_api_id', 'weight', 'player_name']),
    'player_attributes.csv': ('Player_Attributes', None),  # Assuming 'player_attributes.csv' has the correct headers
    'team.csv': ('Team', None),  # Assuming 'team.csv' has the correct headers
    'team_attributes.csv': ('Team_Attributes', None)  # Assuming 'team_attributes.csv' has the correct headers
}

# Function to import CSV data into the corresponding table
def import_csv_to_table(csv_file, table_name, columns_override=None):
    with open(csv_file, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        if columns_override:
            columns = columns_override
            next(reader)  # Skip the header row
        else:
            columns = next(reader)  # Get the column names from the first row
        placeholders = ','.join('?' * len(columns))  # Create placeholders for the column values
        insert_query = f'INSERT OR IGNORE INTO {table_name} ({",".join(columns)}) VALUES ({placeholders})'
        
        for row in reader:
            if 'id' in row[0]:  # Skip rows with column names
                continue
            # Data cleaning and conversion
            new_row = []
            for value, column in zip(row, columns):
                try:
                    if value == '' or value.lower() == 'nan':
                        new_row.append(None)
                    elif column in ['height', 'weight']:
                        new_row.append(float(value))
                    elif column == 'birthday' and '-' in value:
                        new_row.append(datetime.strptime(value, '%Y-%m-%d %H:%M:%S').date())
                    elif column.endswith('_api_id') or column == 'id':
                        new_row.append(int(value))
                    else:
                        new_row.append(value.strip())  # Remove leading/trailing whitespace
                except ValueError:
                    new_row.append(None)  # Insert None if conversion fails

            # Insert the cleaned row into the database
            try:
                cursor.execute(insert_query, new_row)
            except sqlite3.IntegrityError as e:
                print(f"Error inserting row: {new_row}")
                print(f"Error: {e}")

# Import each CSV file into the corresponding table
for csv_file, (table_name, columns_override) in csv_to_table.items():
    import_csv_to_table(csv_file, table_name, columns_override)

# Commit changes and close the connection
conn.commit()
conn.close()
