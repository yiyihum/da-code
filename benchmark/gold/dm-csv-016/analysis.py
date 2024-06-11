import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
from pandasql import sqldf
competitions = pd.read_csv("../competitions.csv")
games = pd.read_csv("../games.csv")
club_games = pd.read_csv("../club_games.csv")
appearances = pd.read_csv("../appearances.csv")
clubs = pd.read_csv("../clubs.csv")
finals = games[(games["round"] == "Final")]

matchdays = games[(games["round"].str.contains("Matchday"))]
matchdays["round"] = matchdays["round"].str.split(".").str.get(0)
matchdays['round'] = matchdays['round'].astype('int')
last_matchday = matchdays.groupby(["competition_id","season"],as_index=False).max("round")
last_matchday = last_matchday[["competition_id","season","round"]]
finals = finals.groupby(["competition_id","season", "round"],as_index=False).sum("home_club_goals")
finals = finals[["competition_id","season", "round"]]
competition = pd.concat([finals,last_matchday])
competition = competition.drop_duplicates().reset_index().drop("index", axis=1)
def league_champions(league):
    
    from pandasql import sqldf
    pysqldf = lambda q: sqldf(q, globals())

    q = f"""

          SELECT 
            g.season,
            case when g.home_club_position = 1 then g.home_club_name
                 when g.away_club_position = 1 then g.away_club_name
                 end as Champion
           FROM games g
           LEFT JOIN competition c
               on c.season = g.season
               and c.competition_id = g.competition_id
           where 
            cast(SUBSTRING(g.round, 1,2) as int) = c.round
           and g.competition_id = '{league}'
           and (g.home_club_position = 1 or g.away_club_position = 1)

           ;"""

    champions = pysqldf(q)
    return champions

def cup_champions(league):
    
    from pandasql import sqldf
    pysqldf = lambda q: sqldf(q, globals())

    q = f"""

          SELECT 
            g.season,
            case when g.home_club_goals > g.away_club_goals then g.home_club_name
                 when g.home_club_goals < g.away_club_goals then g.away_club_name
                 when g.home_club_goals = g.away_club_goals then "draw"
                 else "UNK"
                 end as Champion
           FROM games g
           LEFT JOIN competition c
               on c.season = g.season
               and c.competition_id = g.competition_id
           where
           g.competition_id = '{league}'
           and g.round = c.round
            
           ;"""

    champions = pysqldf(q)
    return champions

def champions(league):
    
    cups = competition[competition["round"] == "Final"]["competition_id"].unique()
    leagues = competition[competition["round"] != "Final"]["competition_id"].unique()
    
    if league in leagues: 
        return league_champions(league)

    if league in cups: 
        return cup_champions(league)
    
    else:
        return "Competition ID not found"
    
# Italian Champions (Seria A)
df1 = champions("IT1")

df1["league"] = ["IT1" for i in range(len(df1))]

df2 = champions("BESC")
df2["league"] = ["BESC" for i in range(len(df2))]
df2 = df2.iloc[1:]

df = pd.concat([df1, df2])
df.to_csv('./result.csv', index=False)

