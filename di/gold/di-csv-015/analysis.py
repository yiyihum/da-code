# %%
# Import Database 

import sqlite3
import pandas as pd

conn = sqlite3.connect('archive(2)\wwe_db.sqlite')

# %% [markdown]
# **6. Which locations held the most number of wrestling events for each promotions?**

# %%
query = f'''
WITH rankings AS (
SELECT 
        p.name AS promotions, 
        l.name AS locations, 
        COUNT(l.name) AS no_of_events,
        ROW_NUMBER() OVER (PARTITION BY p.name ORDER BY COUNT(l.name) DESC) AS ranks
    FROM Locations l 
    INNER JOIN cards c ON l.id = c.location_id 
    INNER JOIN promotions p ON p.id = c.promotion_id 
    GROUP BY l.name, p.name
)
SELECT promotions, locations, no_of_events 
FROM rankings
WHERE ranks = 1;
'''

pd.read_sql(query, conn).to_csv('result.csv')
