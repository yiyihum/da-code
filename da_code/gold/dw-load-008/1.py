import sqlite3
import pandas as pd

# Download and load data using pandas
def download_and_load(url, table_name, conn):
    df = pd.read_csv(url)
    df.to_sql(table_name, conn, if_exists='replace', index=False)

def create_database():
    # Connect to SQLite database
    conn = sqlite3.connect('sports_database.db')

    # Enable foreign key constraint support in SQLite
    conn.execute('PRAGMA foreign_keys = ON;')

    # Create tables
    conn.executescript('''
    DROP TABLE IF EXISTS "athletes";
    CREATE TABLE athletes(
        "id" INTEGER,
        name TEXT,
        gender TEXT,
        age INTEGER,
        height INTEGER,
        weight INTEGER);

    DROP TABLE IF EXISTS "summer_games";
    CREATE TABLE summer_games(
        sport TEXT,
        event TEXT,
        year DATE,
        athlete_id INTEGER,
        country_id INTEGER,
        bronze REAL,
        silver REAL,
        gold REAL);

    DROP TABLE IF EXISTS "winter_games";
    CREATE TABLE winter_games(
        sport TEXT,
        event TEXT,
        year DATE,
        athlete_id INTEGER,
        country_id INTEGER,
        bronze REAL,
        silver REAL,
        gold REAL);

    DROP TABLE IF EXISTS "countries";
    CREATE TABLE countries(
        "id" INTEGER,
        country TEXT,
        region TEXT);

    DROP TABLE IF EXISTS "country_stats";
    CREATE TABLE country_stats(
        "year" TEXT,
        country_id INTEGER,
        gdp REAL,
        pop_in_millions TEXT,
        nobel_prize_winners INTEGER);
    ''')

    # URLs to download CSVs
    urls = {
        'athletes': 'http://assets.datacamp.com/production/repositories/3815/datasets/a5c114363d3f60f514a30683969b1b48b7bc0fe8/athletes_updated.csv',
        'summer_games': 'http://assets.datacamp.com/production/repositories/3815/datasets/174bc4db929ab36891538612c6b1e2cdce11a73b/summer_games_updated.csv',
        'winter_games': 'http://assets.datacamp.com/production/repositories/3815/datasets/1aec560f1e9d22956288a19b1f46f2a21dee0a74/winter_games_updated.csv',
        'countries': 'https://assets.datacamp.com/production/repositories/3815/datasets/3ef4cdfd931e29bc3b1e612d518cf825d56a0362/countries_messy.csv',
        'country_stats': 'http://assets.datacamp.com/production/repositories/3815/datasets/b08d09328a1ab49397e671ee196e957f350bc672/country_stats_updated.csv'
    }

    # Download and load each CSV into the SQLite database
    for table_name, url in urls.items():
        download_and_load(url, table_name, conn)

    conn.close()

if __name__ == '__main__':
    create_database()
