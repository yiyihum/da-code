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
        if isinstance(collection, PathCollection) and len(collection.get_offsets()) > 1:
            return 'scatter'

    # Check for line plots
    lines = ax.get_lines()
    for line in lines:
        if len(line.get_xdata()) > 1 and len(line.get_ydata()) > 1:
            return 'line'
        
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


df1 = pd.read_csv('../closing_odds.csv.gz', index_col=0, compression='gzip')
def result1X2(x):
    if x>0:
        return '1'
    elif x == 0:
        return 'X'
    else:
        return '2'

df1['gol_abs'] = df1.home_score - df1.away_score
df1['result'] = df1.gol_abs.apply(result1X2)

def compute_probs(df_, odd1, oddX, odd2):
    p1 = 'prob1'
    pX = 'probX'
    p2 = 'prob2'
    df_[p1] = 1./df_[odd1]
    df_[pX] = 1./df_[oddX]
    df_[p2] = 1./df_[odd2]
    
    return df_


df1 = compute_probs(df1, 'avg_odds_home_win', 'avg_odds_draw', 'avg_odds_away_win')
def compute_accuracy_and_mean(df_, min_games, n_bins, p1, pX, p2):
    #compute the observed and consensus probabilities
    mean_obs1 = []
    mean_obsX = []
    mean_obs2 = []
    mean_cons1 = []
    mean_consX = []
    mean_cons2 = []
    bins = np.linspace(0,1,n_bins+1)
    
    #pdb.set_trace()
    
    
    for i,bn in enumerate(bins[:-1]):
        # Get the data from the bin
        boole1 = (df_[p1] > bn) & (df_[p1] <= bins[i + 1])
        booleX = (df_[pX] > bn) & (df_[pX] <= bins[i + 1])
        boole2 = (df_[p2] > bn) & (df_[p2] <= bins[i + 1])
        
        # Get accuracy for home, draw away
        if (boole1.sum() >= min_games):
            mean_obs1.append((df_.loc[boole1, 'result'] == '1').sum().astype(float) / boole1.sum())
            mean_cons1.append(df_.loc[boole1, p1].mean())
        else:
            mean_obs1.append(np.nan)
            mean_cons1.append(np.nan)

        if (booleX.sum() >= min_games):
            mean_obsX.append((df_.loc[booleX, 'result'] == 'X').sum().astype(float) / booleX.sum())
            mean_consX.append(df_.loc[booleX, pX].mean())
        else:
            mean_obsX.append(np.nan)
            mean_consX.append(np.nan)
            
        if (boole2.sum() >= min_games):
            mean_obs2.append((df_.loc[boole2, 'result'] == '2').sum().astype(float) / boole2.sum())
            mean_cons2.append(df_.loc[boole2, p2].mean())
        else:
            mean_obs2.append(np.nan)
            mean_cons2.append(np.nan)

        mean_obs_dict = {'1':mean_obs1, 'X':mean_obsX, '2':mean_obs2}
        mean_cons_dict = {'1':mean_cons1, 'X':mean_consX, '2':mean_cons2}
    
    return mean_obs_dict, mean_cons_dict
mean_obs_dict, mean_cons_dict = compute_accuracy_and_mean(df1, 100, 80,'prob1', 'probX', 'prob2')
plt.figure()
plt.scatter(mean_cons_dict['1'], mean_obs_dict['1'], c='blue', s=3, label='home victory')
plt.scatter(mean_cons_dict['X'], mean_obs_dict['X'], c='green', s=3, label='draw')
plt.scatter(mean_cons_dict['2'], mean_obs_dict['2'], c='red', s=3, label='away victory')
plt.xlabel('estimated prob')
plt.ylabel('observed prob')
plt.legend()
plt.savefig('./result.png')




image_parameters = {}
ax, fig = plt.gca(), plt.gcf()
gt_graph = identify_plot_type(ax)

results = []
colors = set()
if gt_graph == 'bar':
    result_data = {'width': [], 'height': []}
    for patch in ax.patches:
        if isinstance(patch, Rectangle):
            width, height = patch.get_width(), patch.get_height()
            result_data['width'].append(width)
            result_data['height'].append(height)
            colors.add(patch.get_facecolor())
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
elif gt_graph  == 'line':
    lines = ax.get_lines()
    for line in lines:
        if len(line.get_xdata()) > 1 and len(line.get_ydata()) > 1:
            results.append(line.get_ydata())
            colors.add(line.get_color())
elif gt_graph  == 'pie':
    result = []
    for patch in ax.patches:
        if isinstance(patch, Wedge):
            result.append(abs(patch.theta2 - patch.theta1) / 360)
            colors.add(patch.get_facecolor())
    results.append(result)
elif gt_graph == 'scatter':
    result =[]
    scatters = [child for child in ax.get_children() if isinstance(child, PathCollection) and len(child.get_offsets()) > 0]
    if scatters:
        for scatter in scatters:
            results.append(scatter.get_offsets().data)
            scatter_colors = scatter.get_facecolor()
            for color in scatter_colors:
                colors.add(tuple(color))

try:
    results = np.array(results) if results else np.array([])
except Exception as e:
    max_length = max(len(x) for x in results)
    results = [np.pad(x, (0, max_length - len(x)), 'constant') for x in results]

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


