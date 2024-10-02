# %%
# Import Database 

import sqlite3
import pandas as pd

conn = sqlite3.connect('archive(2)\wwe_db.sqlite')


# %% [markdown]
# **7. Which wrestlers were involved in the shortest title match for each title in NXT? Give details about the card.**

# %%
query = f'''
SELECT titles, match_duration, matches, win_type, location, event
FROM

(SELECT b.name as titles, 
       m.duration as match_duration, 
       ROW_NUMBER() OVER (PARTITION BY b.name ORDER BY m.duration) AS ranks, 
       w1.name || " vs " || w2.name AS matches, 
       m.win_type win_type, 
       p.name AS promotions, 
       l.name AS location, 
       e.name AS event
       
FROM Belts b 
INNER JOIN Matches m ON m.title_id = b.id
INNER JOIN Wrestlers w1 ON w1.id = m.winner_id 
INNER JOIN Wrestlers w2 ON w2.id = m.loser_id 
INNER JOIN Cards c ON c.id = m.card_id 
INNER JOIN Locations l ON l.id = c.location_id 
INNER JOIN Events e ON e.id = c.event_id 
INNER JOIN promotions p ON p.id = c.promotion_id 

WHERE p.name = 'NXT' AND m.duration <> '' AND b.name <> ''
      AND b.name NOT IN (SELECT name FROM Belts WHERE name LIKE '%title change%')) 

WHERE ranks = 1 
'''

pd.read_sql(query, conn).to_csv('result.csv')
