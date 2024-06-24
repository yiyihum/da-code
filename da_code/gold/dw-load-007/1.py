import sqlite3
import csv
import numpy as np

def calculate_percentile(data, percentile):
    # Using numpy to calculate the percentile
    return np.percentile(data, percentile, interpolation='lower')

def export_table_to_csv(db_connection, query, output_file, percentile=None):
    cursor = db_connection.cursor()
    cursor.execute(query)
    data = cursor.fetchall()

    if percentile is not None:
        # Assuming the profits are the second column in the query result
        profit_values = [row[1] for row in data]
        pct_value = calculate_percentile(profit_values, percentile)
        # Filtering for the sector and appending the calculated percentile
        data = [[row[0], pct_value] for row in data]

    headers = ['sector', 'pct80'] if percentile is not None else [description[0] for description in cursor.description]

    with open(output_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(data)

def main():
    database_path = 'database.db'
    conn = sqlite3.connect(database_path)

    # Query to fetch profits by sector
    fetch_profits_sql = """
    SELECT sector, profits
    FROM fortune500;
    """
    # Exporting profits percentile data to CSV
    export_table_to_csv(conn, fetch_profits_sql, 'profit80.csv')

    # For startdates, since it only involves a simple aggregation (min), SQLite can handle it
    create_startdates_sql = """
    SELECT tag, MIN(date) AS mindate
    FROM stackoverflow
    GROUP BY tag;
    """
    export_table_to_csv(conn, create_startdates_sql, 'startdates.csv')

    conn.close()

if __name__ == '__main__':
    main()
