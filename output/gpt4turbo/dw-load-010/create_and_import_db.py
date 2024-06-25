import sqlite3
import pandas as pd

# Create a new SQLite database
conn = sqlite3.connect('order_customer.db')
cursor = conn.cursor()

# List of CSV files to import
csv_files = ['customers.csv', 'orders.csv', 'order_items.csv']

# Import each CSV file into the database
for csv_file in csv_files:
    # Read the CSV file into a pandas DataFrame
    df = pd.read_csv(f'/workspace/{csv_file}')
    
    # Remove '.csv' from the filename to use as the table name
    table_name = csv_file.replace('.csv', '')
    
    # Import the DataFrame into the SQLite database
    df.to_sql(table_name, conn, if_exists='replace', index=False)

# Commit changes and close the connection
conn.commit()
conn.close()
