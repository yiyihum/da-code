import pandas as pd
import sqlite3

# Create a connection to a new in-memory database
conn = sqlite3.connect(':memory:')

# Assuming you have a CSV file named 'product_emissions.csv'
# Load this CSV file into a DataFrame
df_product_emissions = pd.read_csv('product_emissions.csv')

# Write this DataFrame to a table in the SQLite database
df_product_emissions.to_sql('product_emissions', conn, index=False, if_exists='replace')

# Define the SQL query
sql_query = """
SELECT industry_group,
    COUNT(DISTINCT company) AS num_companies,
    ROUND(SUM(carbon_footprint_pcf), 1) AS total_industry_footprint
FROM product_emissions
WHERE year IN (SELECT MAX(year) FROM product_emissions)
GROUP BY industry_group
ORDER BY total_industry_footprint DESC;
"""

# Execute the query and save the result to a DataFrame
df_result = pd.read_sql_query(sql_query, conn)

# Save the result to a CSV file
df_result.to_csv('result.csv', index=False)

# Close the database connection
conn.close()

# Display the DataFrame to verify the results
df_result
