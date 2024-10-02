# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python Docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

# Input data files are available in the read-only "../input/" directory
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

# You can write up to 20GB to the current directory (/kaggle/working/) that gets preserved as output when you create a version using "Save & Run All" 
# You can also write temporary files to /kaggle/temp/, but they won't be saved outside of the current session

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import sqlite3
import matplotlib.pyplot as plt

# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list the files in the input directory
database = 'archive(1)\\database.sqlite'

conn = sqlite3.connect(database)

tables = pd.read_sql("""SELECT *
                        FROM sqlite_master
                        WHERE type='table';""", conn)

countries = pd.read_sql("""SELECT *
                        FROM Country;""", conn)

leagues = pd.read_sql("""SELECT *
                        FROM League
                        JOIN Country ON Country.id = League.country_id;""", conn)

teams = pd.read_sql("""SELECT *
                        FROM Team
                        ORDER BY team_long_name;""", conn)

detailed_matches = pd.read_sql("""SELECT Match.id, 
                                        Country.name AS country_name, 
                                        League.name AS league_name, 
                                        season, 
                                        stage, 
                                        date,
                                        HT.team_long_name AS  home_team,
                                        AT.team_long_name AS away_team,
                                        home_team_goal, 
                                        away_team_goal                                        
                                FROM Match
                                JOIN Country on Country.id = Match.country_id
                                JOIN League on League.id = Match.league_id
                                LEFT JOIN Team AS HT on HT.team_api_id = Match.home_team_api_id
                                LEFT JOIN Team AS AT on AT.team_api_id = Match.away_team_api_id
                                WHERE country_name = 'Spain'
                                ORDER by date
                                ;""", conn)

detailed_matches.to_csv('detailed_matches.csv')

import pandas as pd

# 计算比分差异
detailed_matches['score_difference'] = abs(detailed_matches['home_team_goal'] - detailed_matches['away_team_goal'])

# 找到比分差异最大的比赛
max_score_difference = detailed_matches.loc[detailed_matches['score_difference'].idxmax()]

# 转置结果并添加列名
max_score_difference = max_score_difference.to_frame().T
max_score_difference.columns = ['id', 'country_name', 'league_name', 'season', 'stage', 'date', 'home_team', 'away_team', 'home_team_goal', 'away_team_goal', 'score_difference']

# 保存结果到CSV文件
max_score_difference.to_csv('max_score_difference.csv', index=False)

