import matplotlib.pyplot as plt
import sys, os, json
from datetime import datetime
import numpy as np
import matplotlib.colors as mcolors
from matplotlib.patches import Wedge, Rectangle
from matplotlib.collections import PathCollection

def identify_plot_type(ax):
    # Check for pie plots
    for patch in ax.patches:
        if isinstance(patch, Wedge):
            return 'pie'

    # Check for bar plots
    for patch in ax.patches:
        if isinstance(patch, Rectangle) and patch.get_width() != patch.get_height():
            return 'bar'

    # Check for scatter plots
    for collection in ax.collections:
        if isinstance(collection, plt.PathCollection):
            return 'scatter'

    # Check for line plots
    lines = ax.get_lines()
    for line in lines:
        if len(line.get_xdata()) > 1 and len(line.get_ydata()) > 1:
            return 'line'
        
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


image_parameters = {}
ax, fig = plt.gca(), plt.gcf()
gt_graph = identify_plot_type(ax)

results = []
colors = []
if gt_graph == 'bar':
    result_data = {'width': [], 'height': []}
    for patch in ax.patches:
        if isinstance(patch, Rectangle):
            width, height = patch.get_width(), patch.get_height()
            result_data['width'].append(width)
            result_data['height'].append(height)
            colors.append(patch.get_facecolor())
    data_type = max(result_data, key=lambda k: len(set(result_data[k])))
    coord_type = 'y' if data_type == 'width' else 'x'
    last_coord = -1000
    result = []
    for patch in ax.patches:
        if not (isinstance(patch, Rectangle)):
            continue
        width = patch.get_width() if data_type == 'height' else patch.get_height()
        if width == 0:
            continue
        coord = patch.get_x() if coord_type == 'x' else patch.get_y()
        if coord < last_coord:
            results.append(result)
            result = []
        result.append(patch.get_height() if data_type == 'height' else patch.get_width())
        last_coord = coord
    if result:
        results.append(result)
    colors = list(set(colors))
elif gt_graph  == 'line':
    lines = ax.get_lines()
    for line in lines:
        results.append(line.get_ydata())
        colors.append(line.get_color())
elif gt_graph  == 'pie':
    for patch in ax.patches:
        if isinstance(patch, Wedge):
            results.append(abs(patch.theta2 - patch.theta1) / 360)
            colors.append(patch.get_facecolor())
elif gt_graph == 'scatter':
    scatters = [child for child in ax.get_children() if isinstance(child, PathCollection)]
    if scatters:
        for scatter in scatters:
            results.append(scatter.get_offsets())
            colors.append(scatter.get_facecolor())

results = np.array(results) if results else np.array([])
if len(results) > 0:
    npy_path = f'./_data_result_{str(datetime.now())}.npy'
    np.save(npy_path, results)
else:
    npy_path = ''

print(results)
print(results.shape)
colors = [str(mcolors.to_hex(rgb_tuple)) for rgb_tuple in colors]
figsize = fig.get_size_inches()
legend = ax.get_legend()
graph_title = ax.get_title() if ax.get_title() else ''
legend_title = legend.get_title().get_text() if legend and legend.get_title() else ''
labels = [text.get_text() for text in legend.get_texts()] if legend else []
x_label = ax.get_xlabel() if ax.get_xlabel() else ''
y_label = ax.get_ylabel() if ax.get_ylabel() else ''
xtick_labels = [label.get_text() for label in ax.get_xticklabels()]
ytick_labels = [label.get_text() for label in ax.get_yticklabels()]

image_parameters['type'] = gt_graph
image_parameters['color'] = colors
image_parameters['figsize'] = list(figsize)
image_parameters['graph_title'] = graph_title
image_parameters['legend_title'] = legend_title
image_parameters['labels'] = labels
image_parameters['x_label'] = x_label 
image_parameters['y_label'] = y_label
image_parameters['xtick_labels'] = xtick_labels
image_parameters['ytick_labels'] = ytick_labels

output_path = f'./_result_image_parameters_{str(datetime.now())}.json'
with open(output_path, 'w') as js:
    json.dump(image_parameters, js)


