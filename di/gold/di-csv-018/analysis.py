# %% [markdown]
# **Initial Setup**

# %%
# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python Docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import sqlite3

# You can write up to 20GB to the current directory (/kaggle/working/) that gets preserved as output when you create a version using "Save & Run All" 
# You can also write temporary files to /kaggle/temp/, but they won't be saved outside of the current session

# %% [markdown]
# In this case 1 means a motorcycle was involved in the collision. And it looks like only a small sample of the overall dataset contain motorcycles. I'll dig deeper into this sample by using the export from the following query to visualize age in this google [sheet](https://docs.google.com/spreadsheets/d/18WpMLaXsEoI7jK9ycoTpSMz7BChAx4ia5gBkk2yL51Q/edit#gid=0). 

# %%
import pandas as pd

# Read CSV files into DataFrames
case_ids_df = pd.read_csv('di-csv-018\\case_ids.csv')
collisions_df = pd.read_csv('di-csv-018\\collisions.csv')
parties_df = pd.read_csv('di-csv-018\\parties.csv')
victims_df = pd.read_csv('di-csv-018\\victims.csv')

# Perform the SQL query 
motorcyclists_killed_by_age_df = pd.merge(collisions_df, parties_df, on='case_id')
motorcyclists_killed_by_age_df = motorcyclists_killed_by_age_df[(motorcyclists_killed_by_age_df['motorcycle_collision'] == 1) & 
                                                              (motorcyclists_killed_by_age_df['party_age'].notnull()) &
                                                              (motorcyclists_killed_by_age_df['motorcyclist_killed_count'] != 0)]
motorcyclists_killed_by_age_df = motorcyclists_killed_by_age_df.groupby(['case_id', 'party_age']).size().reset_index(name='count')
motorcyclists_killed_by_age_df = motorcyclists_killed_by_age_df.sort_values(by='party_age', ascending=False)

# Save the result to a CSV file
motorcyclists_killed_by_age_df.to_csv('motorcyclists_killed_by_age_df.csv', index=False)
                                              


# # %% [markdown]
# # Moving on from age, I am curious to see if motorcyclists who wear helmets are safer. I know I would wear a helmet if I bought a bike so this info might be what convices me. 

# # %%
# motorcyclists_killed_helmet_info = pd.read_sql("""
#                         SELECT 
#                             col.case_id,
#                             party.party_age,
#                             CASE WHEN party.party_safety_equipment_1 = 'driver, motorcycle helmet not used' THEN 1
#                                  ELSE 0 END AS driver_no_helmet,
#                             CASE WHEN party.party_safety_equipment_1 = 'driver, motorcycle helmet used' THEN 1
#                                  ELSE 0 END AS driver_helmet,
#                             CASE WHEN party.party_safety_equipment_2 = 'driver, motorcycle helmet not used' THEN 1
#                                  ELSE 0 END AS driver_no_helmet2,
#                             CASE WHEN party.party_safety_equipment_2 = 'driver, motorcycle helmet used' THEN 1
#                                  ELSE 0 END AS driver_helmet2,
#                             CASE WHEN party.party_safety_equipment_1 = 'passenger, motorcycle helmet not used' THEN 1
#                                  ELSE 0 END AS psngr_no_helmet,
#                             CASE WHEN party.party_safety_equipment_1 = 'passenger, motorcycle helmet used' THEN 1
#                                  ELSE 0 END AS psngr_helmet,
#                             CASE WHEN party.party_safety_equipment_2 = 'passenger, motorcycle helmet not used' THEN 1
#                                  ELSE 0 END AS psngr_no_helmet,
#                             CASE WHEN party.party_safety_equipment_2 = 'passenger, motorcycle helmet used' THEN 1
#                                  ELSE 0 END AS psngr_helmet
#                         FROM collisions col
#                         JOIN parties party
#                             ON col.case_id = party.case_id
#                         WHERE 
#                         col.motorcycle_collision = 1
#                         AND party.party_age IS NOT NULL
#                         AND col.motorcyclist_killed_count != 0
#                         GROUP BY 1, 2
#                         """, conn)

# motorcyclists_killed_helmet_info = pd.DataFrame(motorcyclists_killed_helmet_info)
# motorcyclists_killed_helmet_info.to_csv('motorcyclists_killed_helmet_info.csv',index=False)

# # %% [markdown]
# # It looks like there are a lot more deaths of motorcyclists who wear helmets than those who don't? But I've always been told that helmets are safer! Lets see what percent of the population who don't wear helmets have died in collisions. 

# # %%
# no_helmet_accident_death_percent = pd.read_sql("""
#                         WITH base AS (
#                             SELECT 
#                                 col.case_id AS case_id,
#                                 col.motorcyclist_killed_count AS motorcyclist_killed_count,
#                                 CASE WHEN party.party_safety_equipment_1 = 'driver, motorcycle helmet not used' THEN 1
#                                     ELSE 0 END AS driver_no_helmet,
#                                 CASE WHEN party.party_safety_equipment_2 = 'driver, motorcycle helmet not used' THEN 1
#                                     ELSE 0 END AS driver_no_helmet2,
#                                 CASE WHEN party.party_safety_equipment_1 = 'passenger, motorcycle helmet not used' THEN 1
#                                     ELSE 0 END AS psngr_no_helmet,
#                                 CASE WHEN party.party_safety_equipment_2 = 'passenger, motorcycle helmet not used' THEN 1
#                                     ELSE 0 END AS psngr_no_helmet2
#                             FROM collisions col
#                             JOIN parties party
#                                 ON col.case_id = party.case_id
#                             WHERE 
#                             col.motorcycle_collision = 1
#                             AND party.party_age IS NOT NULL
#                             GROUP BY 1, 2
#                         ),
#                         counts AS (
#                             SELECT 
#                                 case_id,
#                                 motorcyclist_killed_count
#                             FROM base
#                             WHERE
#                             driver_no_helmet = 1
#                             OR driver_no_helmet2 = 1 
#                             OR psngr_no_helmet = 1 
#                             OR psngr_no_helmet2 = 1
#                         )
#                         SELECT 
#                             ROUND(SUM(CAST(motorcyclist_killed_count AS FLOAT)) * 100 / COUNT(*), 2) AS percent_killed
#                         FROM 
#                             counts
                        
#                         """, conn)

# no_helmet_accident_death_percent = pd.DataFrame(no_helmet_accident_death_percent)
# no_helmet_accident_death_percent.to_csv('no_helmet_accident_death_percent.csv',index=False)

# # %% [markdown]
# # Now let's look at the same metric for riders who wear helmets. 

# # %%
# helmet_accident_death_percent = pd.read_sql("""
#                         WITH base AS (
#                             SELECT 
#                                 col.case_id AS case_id,
#                                 col.motorcyclist_killed_count AS motorcyclist_killed_count,
#                             CASE WHEN party.party_safety_equipment_1 = 'driver, motorcycle helmet used' THEN 1
#                                  ELSE 0 END AS driver_helmet,
#                             CASE WHEN party.party_safety_equipment_2 = 'driver, motorcycle helmet used' THEN 1
#                                  ELSE 0 END AS driver_helmet2,
#                             CASE WHEN party.party_safety_equipment_1 = 'passenger, motorcycle helmet used' THEN 1
#                                  ELSE 0 END AS psngr_helmet,
#                             CASE WHEN party.party_safety_equipment_2 = 'passenger, motorcycle helmet used' THEN 1
#                                  ELSE 0 END AS psngr_helmet2
#                             FROM collisions col
#                             JOIN parties party
#                                 ON col.case_id = party.case_id
#                             WHERE 
#                             col.motorcycle_collision = 1
#                             AND party.party_age IS NOT NULL
#                             GROUP BY 1, 2
#                         ),
#                         counts AS (
#                             SELECT 
#                                 case_id,
#                                 motorcyclist_killed_count
#                             FROM base
#                             WHERE
#                             driver_helmet = 1
#                             OR driver_helmet2 = 1
#                             OR psngr_helmet = 1
#                             OR psngr_helmet2 = 1
#                         )
#                         SELECT 
#                             ROUND(SUM(CAST(motorcyclist_killed_count AS FLOAT)) * 100 / COUNT(*), 2) AS percent_killed
#                         FROM 
#                             counts
                        
#                         """, conn)

# helmet_accident_death_percent = pd.DataFrame(helmet_accident_death_percent)
# helmet_accident_death_percent.to_csv('helmet_accident_death_percent.csv',index=False)

# # %% [markdown]
# # Wow 3.55% is still pretty high! I think even with a helmet motorcycles are dangerous, but that could be part of the fun for some people?
# # Don't forget to see the visualizations for this notebook [here](https://docs.google.com/spreadsheets/d/18WpMLaXsEoI7jK9ycoTpSMz7BChAx4ia5gBkk2yL51Q/edit#gid=0)

# # %%

# conn.close()

