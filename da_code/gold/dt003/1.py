import pandas as pd
import sqlite3

# Create a connection to a new in-memory database
conn = sqlite3.connect(':memory:')

# Assuming you have CSV files named 'donations.csv' and 'assignments.csv'
# Load these CSV files into DataFrames
df_donations = pd.read_csv('donations.csv')
df_assignments = pd.read_csv('assignments.csv')

# Write these DataFrames to tables in the SQLite database
df_donations.to_sql('donations', conn, index=False, if_exists='replace')
df_assignments.to_sql('assignments', conn, index=False, if_exists='replace')

# Define the SQL query
sql_query = """
WITH donation_counts AS (
    SELECT
        assignment_id,
        COUNT(donation_id) AS num_total_donations
    FROM
        donations
    GROUP BY
        assignment_id
),
ranked_assignments AS (
    SELECT
        a.assignment_name,
        a.region,
        a.impact_score,
        dc.num_total_donations,
        ROW_NUMBER() OVER (PARTITION BY a.region ORDER BY a.impact_score DESC) AS rank_in_region
    FROM
        assignments a
    JOIN
        donation_counts dc ON a.assignment_id = dc.assignment_id
    WHERE
        dc.num_total_donations > 0
)
SELECT
    assignment_name,
    region,
    impact_score,
    num_total_donations
FROM
    ranked_assignments
WHERE
    rank_in_region = 1
ORDER BY
    region ASC;
"""

# Execute the query and save the result to a DataFrame
df_result = pd.read_sql_query(sql_query, conn)

# Save the result to a CSV file
df_result.to_csv('result.csv', index=False)

# Close the database connection
conn.close()

# Display the DataFrame to verify the results
df_result
