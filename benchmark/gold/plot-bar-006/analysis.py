import pandas as pd
import matplotlib.pyplot as plt

Core_Match_Data = pd.read_csv('../results.csv')
Goal_Scoring_Specifics = pd.read_csv('../goalscorers.csv')
Penalty_Shootout_Details = pd.read_csv('../shootouts.csv')

home_wins = Core_Match_Data[Core_Match_Data['home_score'] > Core_Match_Data['away_score']]['home_team'].value_counts()
away_wins = Core_Match_Data[Core_Match_Data['away_score'] > Core_Match_Data['home_score']]['away_team'].value_counts()
total_matches_home = Core_Match_Data['home_team'].value_counts()
total_matches_away = Core_Match_Data['away_team'].value_counts()

total_wins = home_wins.add(away_wins, fill_value=0)
win_percentages = (total_wins / (total_matches_home + total_matches_away) * 100).sort_values(ascending=False)

top_3_teams = win_percentages.head(3)
df_top_3 = top_3_teams.reset_index()
df_top_3.columns = ['Team Name', 'Win Percentage']
df_top_3.to_csv('./result.csv', index=False)

matches_2000_to_2023 = Core_Match_Data[(Core_Match_Data['date'] >= '2000-01-01') & (Core_Match_Data['date'] <= '2023-12-31')]

team_performance_2000_to_2023 = matches_2000_to_2023.groupby('home_team').agg({
    'home_score': 'mean',
    'away_score': 'mean',
    'tournament': 'count',
    'neutral': 'sum'
}).reset_index()
team_performance_2000_to_2023.columns = ['Team', 'Average_Home_Score', 'Average_Away_Score', 'Matches_Played', 'Neutral_Ground']

team_performance_2000_to_2023['Overall_Score'] = team_performance_2000_to_2023['Matches_Played'] + 2 * team_performance_2000_to_2023['Neutral_Ground']

best_teams_2000_to_2023 = team_performance_2000_to_2023.sort_values(by='Overall_Score', ascending=False).head(10)

plt.figure(figsize=(12, 8))
plt.bar(best_teams_2000_to_2023['Team'], best_teams_2000_to_2023['Overall_Score'], color='skyblue')

plt.title('Best Teams from 2000 to 2023', fontsize=20, fontweight='bold')
plt.xlabel('Football Team', fontsize=14)
plt.ylabel('Overall Score', fontsize=14)
plt.xticks(rotation=45, ha='right', fontsize=12)

plt.tight_layout()
plt.savefig('team.png', dpi=300)
