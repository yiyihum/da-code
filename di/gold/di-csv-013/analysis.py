# %%
# Import Database 

import sqlite3
import pandas as pd

conn = sqlite3.connect('archive(2)\wwe_db.sqlite')

# %% [markdown]
# **4. How many title belts are there for each promotion and gender?**
# 
# We only considered titles which have the promotion name in the title name itself (Eg. NXT Women's Title). 
# 
# We excluded some title name that consists of the phrase "title change". We did not count Money in the Bank Briefcase, King of the Ring, spot in the Royal Rumble, interim championships and Dusty Rhodes Tag Team Classic Cup as titles. 
# 
# We assumed that titles with the phrases "female", "women" and "diva" are considered titles for female wrestlers.

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


SELECT promotions, gender, COUNT(*) AS number_of_titles
FROM (
    SELECT 
        CASE 
            WHEN name LIKE '%WWE%' THEN 'WWE'
            WHEN name LIKE '%WWF%' THEN 'WWF'
            WHEN name LIKE '%WWWF%' THEN 'WWWF'
            WHEN name LIKE '%WCW%' THEN 'WCW'
            WHEN name LIKE '%NXT%' THEN 'NXT'
            ELSE 'ECW'
        END AS promotions, 
        
        CASE 
           WHEN LOWER(name) LIKE '%women%' THEN 'Female'
           WHEN LOWER(name) LIKE '%female%' THEN 'Female'
           WHEN LOWER(name) LIKE '%Diva%' THEN 'Female'
           ELSE 'Male'
        END AS gender
        
    FROM Titles
) AS Title_Details
GROUP BY promotions, gender 
'''

pd.read_sql(query, conn).to_csv('result.csv')