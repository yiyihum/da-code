import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sqlite3

db = '../database.sqlite'
conn = sqlite3.connect(db)
master_table = pd.read_sql("""SELECT * 
                    FROM sqlite_master
                    WHERE type='table';""", conn)
all_star_table= pd.read_sql("""SELECT *
                        FROM all_star;""", conn)
appearances_table= pd.read_sql("""SELECT *
                        FROM appearances;""", conn)
batting_table= pd.read_sql("""SELECT *
                        FROM batting;""", conn)
batting_postseason_table= pd.read_sql("""SELECT *
                        FROM batting_postseason;""", conn)
college_table= pd.read_sql("""SELECT *
                        FROM college;""", conn)
fielding_table= pd.read_sql("""SELECT *
                        FROM fielding;""", conn)
fielding_outfield_table= pd.read_sql("""SELECT *
                        FROM fielding_outfield;""", conn)
fielding_postseason_table= pd.read_sql("""SELECT *
                        FROM fielding_postseason;""", conn)
hall_of_fame_table= pd.read_sql("""SELECT *
                        FROM hall_of_fame;""", conn)
home_game_table= pd.read_sql("""SELECT *
                        FROM home_game;""", conn)
manager_table= pd.read_sql("""SELECT *
                        FROM manager;""", conn)
manager_award_table= pd.read_sql("""SELECT *
                        FROM manager_award;""", conn)
manager_award_vote_table= pd.read_sql("""SELECT *
                        FROM manager_award_vote;""", conn)
manager_half_table= pd.read_sql("""SELECT *
                        FROM manager_half;""", conn)
player_table= pd.read_sql("""SELECT *
                        FROM player;""", conn)
park_table= pd.read_sql("""SELECT *
                        FROM park;""", conn)

sql = pd.read_sql(
"""
select 'Most Games Played :- '|| t.player_name as Player_Name,max(t.games_played) as Batting_Table_Topper
from
(select
b.player_id,
p.name_given as player_name,
b.team_id,
sum(b.g) as games_played,
b.ab as at_bats,
sum(b.r) as runs,
b.h as hits,
b.double as doubles,
b.triple as triples,
b.hr as  Home_runs,
b.rbi as Run_batted_in, 
b.sb as Stolen_Bases, 
b.cs as Caught_Stealing,
b.bb as Walks, 
b.so as Strikeouts,
b.ibb as intentional_base_on_balls, 
b.hbp as hit_by_pitch, 
b.sh as sacrifice_bunt ,
b.sf as sacrifice_flies ,
b.g_idp as Ground_into_double_play
from player p
join batting b on
p.player_id=b.player_id
group by b.player_id) t

union all

select 'Most Runs :- '|| t.player_name as player_name,max(t.runs) as Batting_Table_Topper
from
(select
b.player_id,
p.name_given as player_name,
b.team_id,
sum(b.g) as games_played,
b.ab as at_bats,
sum(b.r) as runs,
b.h as hits,
b.double as doubles,
b.triple as triples,
b.hr as  Home_runs,
b.rbi as Run_batted_in, 
b.sb as Stolen_Bases, 
b.cs as Caught_Stealing,
b.bb as Walks, 
b.so as Strikeouts,
b.ibb as intentional_base_on_balls, 
b.hbp as hit_by_pitch, 
b.sh as sacrifice_bunt ,
b.sf as sacrifice_flies ,
b.g_idp as Ground_into_double_play
from player p
join batting b on
p.player_id=b.player_id
group by b.player_id) t

union all

select 'Most Hits :- '|| t.player_name as player_name,max(t.hits) as Batting_Table_Topper
from
(select
b.player_id,
p.name_given as player_name,
b.team_id,
sum(b.g) as games_played,
b.ab as at_bats,
sum(b.r) as runs,
sum(b.h) as hits,
b.double as doubles,
b.triple as triples,
b.hr as  Home_runs,
b.rbi as Run_batted_in, 
b.sb as Stolen_Bases, 
b.cs as Caught_Stealing,
b.bb as Walks, 
b.so as Strikeouts,
b.ibb as intentional_base_on_balls, 
b.hbp as hit_by_pitch, 
b.sh as sacrifice_bunt ,
b.sf as sacrifice_flies ,
b.g_idp as Ground_into_double_play
from player p
join batting b on
p.player_id=b.player_id
group by b.player_id) t

union all

select 'Most Home Runs :- '|| t.player_name as player_name,max(t.Home_Runs) as Batting_Table_Topper
from
(select
b.player_id,
p.name_given as player_name,
b.team_id,
sum(b.g) as games_played,
b.ab as at_bats,
sum(b.r) as runs,
sum(b.h) as hits,
sum(b.double) as doubles,
sum(b.triple) as triples,
sum(b.hr) as  Home_runs,
b.rbi as Run_batted_in, 
b.sb as Stolen_Bases, 
b.cs as Caught_Stealing,
b.bb as Walks, 
b.so as Strikeouts,
b.ibb as intentional_base_on_balls, 
b.hbp as hit_by_pitch, 
b.sh as sacrifice_bunt ,
b.sf as sacrifice_flies ,
b.g_idp as Ground_into_double_play
from player p
join batting b on
p.player_id=b.player_id
group by b.player_id) t



""", conn)

sql.to_csv("./result.csv", index=False)
