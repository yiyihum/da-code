import sqlite3
import csv

def load_csv_to_sqlite(db_path, csv_file_path):
    # Connect to the SQLite database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Optional: Create the table if not exists (Ensure to adjust fields and types as needed)
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS stackoverflow (
        tag TEXT,
        date TEXT,
        question_count INTEGER,
        question_pct REAL,
        unanswered_count INTEGER,
        unanswered_pct REAL
    );
    ''')

    # Open the CSV file
    with open(csv_file_path, newline='') as csvfile:
        # Create a CSV reader object
        reader = csv.DictReader(csvfile)
        
        # Iterate over the CSV rows
        for row in reader:
            # Prepare data for insertion (convert types if necessary)
            data = (
                row['tag'],
                row['date'],
                int(row['question_count']),
                float(row['question_pct']),
                int(row['unanswered_count']),
                float(row['unanswered_pct'])
            )
            
            # Insert data into the table
            cursor.execute('''
            INSERT INTO stackoverflow (tag, date, question_count, question_pct, unanswered_count, unanswered_pct)
            VALUES (?, ?, ?, ?, ?, ?);
            ''', data)
    
    # Commit the changes and close the connection
    conn.commit()
    cursor.close()
    conn.close()

if __name__ == '__main__':
    database_path = 'database.db'
    csv_path = 'stackoverflow.csv'
    load_csv_to_sqlite(database_path, csv_path)
