import sqlite3
import csv

# Connect to the sport.db database
conn = sqlite3.connect('sport.db')
cursor = conn.cursor()

# A dictionary mapping CSV file names to their corresponding table names
csv_to_table = {
    'country_info.csv': 'Country',
    'league_info.csv': 'League',
    'match.csv': 'Match',
    'player.csv': 'Player',
    'player_attributes.csv': 'Player_Attributes',
    'team.csv': 'Team',
    'team_attributes.csv': 'Team_Attributes'
}

# Function to import CSV data into the corresponding table
def import_csv_to_table(csv_file, table_name):
    with open(csv_file, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        columns = next(reader)  # Get the column names from the first row
        placeholders = ','.join('?' * len(columns))  # Create placeholders for the column values
        insert_query = f'INSERT INTO {table_name} ({",".join(columns)}) VALUES ({placeholders})'
        
        for row in reader:
            cursor.execute(insert_query, row)

# Import each CSV file into the corresponding table
for csv_file, table_name in csv_to_table.items():
    import_csv_to_table(csv_file, table_name)

# Commit changes and close the connection
conn.commit()
conn.close()
