import sqlite3
import csv

# Connect to the sport.db database
conn = sqlite3.connect('sport.db')
cursor = conn.cursor()

# A dictionary mapping CSV file names to their corresponding table names and columns
csv_to_table = {
    'country_info.csv': ('Country', None),
    'league_info.csv': ('League', None),
    'match.csv': ('Match', None),
    'player.csv': ('Player', ['id', 'player_api_id', 'player_name', 'player_fifa_api_id', 'birthday', 'height', 'weight']),
    'player_attributes.csv': ('Player_Attributes', None),
    'team.csv': ('Team', None),
    'team_attributes.csv': ('Team_Attributes', None)
}

# Function to import CSV data into the corresponding table
def import_csv_to_table(csv_file, table_name, columns_override=None):
    with open(csv_file, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        columns = next(reader)  # Get the column names from the first row
        if columns_override:
            columns = columns_override
        placeholders = ','.join('?' * len(columns))  # Create placeholders for the column values
        insert_query = f'INSERT INTO {table_name} ({",".join(columns)}) VALUES ({placeholders})'
        
        for row in reader:
            cursor.execute(insert_query, row)

# Import each CSV file into the corresponding table
for csv_file, (table_name, columns_override) in csv_to_table.items():
    import_csv_to_table(csv_file, table_name, columns_override)

# Commit changes and close the connection
conn.commit()
conn.close()
