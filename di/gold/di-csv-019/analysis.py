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
                         
import pandas as pd

# Read CSV files into DataFrames
case_ids_df = pd.read_csv('di-csv-018/case_ids.csv')
collisions_df = pd.read_csv('di-csv-018/collisions.csv')
parties_df = pd.read_csv('di-csv-018/parties.csv')
victims_df = pd.read_csv('di-csv-018/victims.csv')

# Perform the query on the CSV data
motorcyclists_killed_helmet_info = collisions_df.merge(parties_df, on='case_id')
motorcyclists_killed_helmet_info = motorcyclists_killed_helmet_info[(motorcyclists_killed_helmet_info['motorcycle_collision'] == 1) & (motorcyclists_killed_helmet_info['party_age'].notnull()) & (motorcyclists_killed_helmet_info['motorcyclist_killed_count'] != 0)]
motorcyclists_killed_helmet_info['driver_no_helmet'] = (motorcyclists_killed_helmet_info['party_safety_equipment_1'] == 'driver, motorcycle helmet not used').astype(int)
motorcyclists_killed_helmet_info['driver_helmet'] = (motorcyclists_killed_helmet_info['party_safety_equipment_1'] == 'driver, motorcycle helmet used').astype(int)
motorcyclists_killed_helmet_info['driver_no_helmet2'] = (motorcyclists_killed_helmet_info['party_safety_equipment_2'] == 'driver, motorcycle helmet not used').astype(int)
motorcyclists_killed_helmet_info['driver_helmet2'] = (motorcyclists_killed_helmet_info['party_safety_equipment_2'] == 'driver, motorcycle helmet used').astype(int)
motorcyclists_killed_helmet_info['psngr_no_helmet'] = (motorcyclists_killed_helmet_info['party_safety_equipment_1'] == 'passenger, motorcycle helmet not used').astype(int)
motorcyclists_killed_helmet_info['psngr_helmet'] = (motorcyclists_killed_helmet_info['party_safety_equipment_1'] == 'passenger, motorcycle helmet used').astype(int)
motorcyclists_killed_helmet_info['psngr_no_helmet2'] = (motorcyclists_killed_helmet_info['party_safety_equipment_2'] == 'passenger, motorcycle helmet not used').astype(int)
motorcyclists_killed_helmet_info['psngr_helmet2'] = (motorcyclists_killed_helmet_info['party_safety_equipment_2'] == 'passenger, motorcycle helmet used').astype(int)

# Save the result as a CSV file
motorcyclists_killed_helmet_info.to_csv('motorcyclists_killed_helmet_info.csv', index=False)

