# %%
# Import Database 

import sqlite3
import pandas as pd

conn = sqlite3.connect('archive(2)\wwe_db.sqlite')

# %%
query = f''' 
SELECT 
SUM(CASE WHEN LENGTH (name) - LENGTH(REPLACE(name, '&', '')) = 0 THEN 1 ELSE 0 END) No_of_Individual_Wrestlers, 
SUM(CASE WHEN LENGTH (name) - LENGTH(REPLACE(name, '&', '')) = 1 THEN 1 ELSE 0 END) No_of_Tag_Teams, 
SUM(CASE WHEN LENGTH (name) - LENGTH(REPLACE(name, '&', '')) = 2 THEN 1 ELSE 0 END) No_of_Triple_Teams, 
SUM(CASE WHEN LENGTH (name) - LENGTH(REPLACE(name, '&', '')) > 2 THEN 1 ELSE 0 END) No_of_Teams_with_More_Than_3_Members
FROM Wrestlers
'''

pd.read_sql_query(query, conn).to_csv('1.csv')

# %%
query = f'''
SELECT name 
FROM Wrestlers 
WHERE LENGTH (name) - LENGTH(REPLACE(name, '&', '')) > 2
LIMIT 20
'''

pd.read_sql(query, conn).to_csv('2.csv')
