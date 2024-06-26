import sqlite3

# Define the schema based on the provided schema.yml
schema = {
    'wrestlers': '''
        CREATE TABLE IF NOT EXISTS wrestlers (
            id INTEGER PRIMARY KEY,
            name TEXT
        )
    ''',
    'belts': '''
        CREATE TABLE IF NOT EXISTS belts (
            id INTEGER PRIMARY KEY,
            name TEXT
        )
    ''',
    'cards': '''
        CREATE TABLE IF NOT EXISTS cards (
            id INTEGER PRIMARY KEY,
            table_id INTEGER,
            location_id INTEGER,
            promotion_id INTEGER,
            event_date DATE,
            event_id INTEGER,
            url TEXT,
            info_html TEXT,
            match_html TEXT
        )
    ''',
    'events': '''
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY,
            name TEXT
        )
    ''',
    'locations': '''
        CREATE TABLE IF NOT EXISTS locations (
            id INTEGER PRIMARY KEY,
            name TEXT
        )
    ''',
    'matches': '''
        CREATE TABLE IF NOT EXISTS matches (
            id INTEGER PRIMARY KEY,
            card_id INTEGER,
            winner_id INTEGER,
            win_type TEXT,
            loser_id INTEGER,
            match_type_id INTEGER,
            duration TIME,
            title_id INTEGER,
            title_change INTEGER
        )
    ''',
    'promotions': '''
        CREATE TABLE IF NOT EXISTS promotions (
            id INTEGER PRIMARY KEY,
            name TEXT
        )
    '''
}

# Connect to the SQLite database
conn = sqlite3.connect('wwe.db')
cursor = conn.cursor()

# Create tables
for table_name, table_schema in schema.items():
    cursor.execute(table_schema)

# Commit changes and close the connection
conn.commit()
conn.close()
