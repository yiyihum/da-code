import pandas as pd
import sqlite3

# Create a connection to a new in-memory database
conn = sqlite3.connect(':memory:')

# Assuming you have CSV files named 'donations.csv', 'donors.csv', and 'assignments.csv'
# Load these CSV files into DataFrames
df_donations = pd.read_csv('donations.csv')
df_donors = pd.read_csv('donors.csv')
df_assignments = pd.read_csv('assignments.csv')

# Write these DataFrames to tables in the SQLite database
df_donations.to_sql('donations', conn, index=False, if_exists='replace')
df_donors.to_sql('donors', conn, index=False, if_exists='replace')
df_assignments.to_sql('assignments', conn, index=False, if_exists='replace')

# Define the SQL query
sql_query = """
WITH donation_details AS (
    SELECT
        d.assignment_id,
        ROUND(SUM(d.amount), 2) AS rounded_total_donation_amount,
        dn.donor_type
    FROM
        donations d
    JOIN donors dn ON d.donor_id = dn.donor_id
    GROUP BY
        d.assignment_id, dn.donor_type
)
SELECT
    a.assignment_name,
    a.region,
    dd.rounded_total_donation_amount,
    dd.donor_type
FROM
    assignments a
JOIN
    donation_details dd ON a.assignment_id = dd.assignment_id
ORDER BY
    dd.rounded_total_donation_amount DESC
LIMIT 5;
"""

# Execute the query and save the result to a DataFrame
df_result = pd.read_sql_query(sql_query, conn)

# Save the result to a CSV file
df_result.to_csv('result.csv', index=False)

# Close the database connection
conn.close()

df_result
