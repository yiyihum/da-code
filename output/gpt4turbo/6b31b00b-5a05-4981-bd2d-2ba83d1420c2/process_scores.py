import pandas as pd
import matplotlib.pyplot as plt
import yaml
from datetime import datetime

# Load the results data
df = pd.read_csv('/workspace/results.csv')

# Filter the data for the past 23 years
current_year = datetime.now().year
df['date'] = pd.to_datetime(df['date'])
df = df[df['date'].dt.year > current_year - 23]

# Calculate the total scores for each team
df['total_score'] = df['home_score'] + df['away_score']
team_scores = df.groupby('home_team')['home_score'].sum().add(df.groupby('away_team')['away_score'].sum(), fill_value=0)

# Identify the top 10 teams
top_teams = team_scores.nlargest(10)

# Load the plot configuration from 'plot.yaml'
with open('/workspace/plot.yaml', 'r') as file:
    plot_config = yaml.safe_load(file)

# Generate the bar chart
plt.figure(figsize=tuple(plot_config['figsize']))
plt.bar(top_teams.index, top_teams.values, color=plot_config['color'])
plt.title(plot_config['graph_title'])
plt.xlabel(plot_config['x_label'])
plt.ylabel(plot_config['y_label'])
plt.xticks(rotation=45)  # Assuming a standard rotation for readability
plt.tight_layout()

# Save the bar chart image
plt.savefig('/workspace/team.png')
