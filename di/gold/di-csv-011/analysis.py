# %%
# Import Database 

import sqlite3
import pandas as pd

conn = sqlite3.connect('archive(2)\wwe_db.sqlite')

# %% [markdown]
# **2. How many titles belts are there in total?**
# 
# We excluded some title name that consists of the phrase "title change". We did not count Money in the Bank Briefcase, King of the Ring, spot in the Royal Rumble, interim championships and Dusty Rhodes Tag Team Classic Cup as titles. 

# %%
query = f'''
SELECT COUNT(*) AS Number_of_Titles 
FROM Belts
WHERE name NOT IN (SELECT name FROM Belts WHERE name LIKE '%title change%') 
AND name NOT IN (SELECT name FROM Belts WHERE name LIKE '%Briefcase%' )
AND name NOT IN (SELECT name FROM Belts WHERE name LIKE '%King of the Ring%')
AND name NOT IN (SELECT name FROM Belts WHERE name LIKE '%Royal Rumble%')
AND name NOT IN (SELECT name FROM Belts WHERE name LIKE '%Dusty Rhodes%')
AND name NOT IN (SELECT name FROM Belts WHERE name LIKE '%Interim%')
'''

pd.read_sql(query, conn).to_csv('1.csv')

# %%
query = f'''
SELECT * 
FROM Belts
WHERE name NOT IN (SELECT name FROM Belts WHERE name LIKE '%title change%') 
AND name NOT IN (SELECT name FROM Belts WHERE name LIKE '%Briefcase%' )
AND name NOT IN (SELECT name FROM Belts WHERE name LIKE '%King of the Ring%')
AND name NOT IN (SELECT name FROM Belts WHERE name LIKE '%Royal Rumble%')
AND name NOT IN (SELECT name FROM Belts WHERE name LIKE '%Dusty Rhodes%')
AND name NOT IN (SELECT name FROM Belts WHERE name LIKE '%Interim%')
'''

pd.read_sql(query, conn).to_csv('2.csv')
