import sqlite3
import pandas as pd

# Create a new SQLite database
db_connection = sqlite3.connect('database.db')

# Function to load a CSV file into the database
def load_csv_to_db(csv_file, table_name):
    # Read the CSV file into a pandas DataFrame
    df = pd.read_csv(csv_file)
    
    # Remove any existing table with the same name
    db_connection.execute(f"DROP TABLE IF EXISTS {table_name}")
    
    # Write the data to a SQLite table
    df.to_sql(table_name, db_connection, if_exists='replace', index=False)

# Load each CSV file into the database
load_csv_to_db('Salaries_part1.csv', 'Salaries_part1')
load_csv_to_db('Salaries_part2.csv', 'Salaries_part2')
load_csv_to_db('Salaries_part3.csv', 'Salaries_part3')

# Close the database connection
db_connection.close()
