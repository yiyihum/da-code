# %%
# Import Database 

import sqlite3
import pandas as pd

conn = sqlite3.connect('archive(2)\wwe_db.sqlite')

# %% [markdown]
# **8. Which wrestlers had the highest win rate at Elimination Chamber respectively?**

# %%
query = f'''
SELECT wrestlers, no_of_wins 
FROM

(SELECT w.name AS wrestlers, COUNT(m.winner_id) AS no_of_wins, 
       RANK() OVER (ORDER BY COUNT(m.winner_id) DESC) AS ranks 
FROM Wrestlers w 
INNER JOIN Matches m ON m.winner_id = w.id 
INNER JOIN Cards c ON c.id = m.card_id
INNER JOIN Events e ON e.id = c.event_id 
WHERE LOWER(e.name) LIKE '%elimination chamber%'
GROUP BY w.name) 

WHERE ranks BETWEEN 1 AND 3 
'''

pd.read_sql(query, conn).to_csv('result.csv')

# %% [markdown]
# #### **Thank you for reading my notebook. If you like the notebook, help to give it an upvote.**


