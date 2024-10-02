# %%
# Import Database 

import sqlite3
import pandas as pd

conn = sqlite3.connect('archive(2)\wwe_db.sqlite')

# %% [markdown]
# **5. How many title belts are for tag teams in each promotion?**
# 
# We only considered titles which have the promotion name in the title name itself (Eg. NXT Women's Title). 
# 
# We excluded some title name that consists of the phrase "title change". We did not count Money in the Bank Briefcase, King of the Ring, spot in the Royal Rumble, interim championships and Dusty Rhodes Tag Team Classic Cup as titles. 
# 
# We assumed that tag team titles will have the phrase "tag team" in the title name.

# %%
query = f'''
WITH Titles AS (
    SELECT name 
    FROM Belts 
    WHERE name LIKE '%WWE%' OR name LIKE '%WWF%' OR name LIKE '%WWWF%' OR name LIKE '%WCW%' OR name LIKE '%NXT%' OR name LIKE '%ECW%'
    AND name NOT IN (SELECT name FROM Belts WHERE name LIKE '%title change%') 
    AND name NOT IN (SELECT name FROM Belts WHERE name LIKE '%Briefcase%' )
    AND name NOT IN (SELECT name FROM Belts WHERE name LIKE '%King of the Ring%')
    AND name NOT IN (SELECT name FROM Belts WHERE name LIKE '%Royal Rumble%')
    AND name NOT IN (SELECT name FROM Belts WHERE name LIKE '%Dusty Rhodes%')
    AND name NOT IN (SELECT name FROM Belts WHERE name LIKE '%Interim%')
)


SELECT promotions, COUNT(*) AS number_of_titles
FROM (
    SELECT name, 
        CASE 
            WHEN name LIKE '%WWE%' THEN 'WWE'
            WHEN name LIKE '%WWF%' THEN 'WWF'
            WHEN name LIKE '%WWWF%' THEN 'WWWF'
            WHEN name LIKE '%WCW%' THEN 'WCW'
            WHEN name LIKE '%NXT%' THEN 'NXT'
            ELSE 'ECW'
        END AS promotions
        
    FROM Titles
) AS Title_Details
WHERE LOWER(name) LIKE '%tag team%'
GROUP BY promotions 
'''

pd.read_sql(query, conn).to_csv('result.csv')
