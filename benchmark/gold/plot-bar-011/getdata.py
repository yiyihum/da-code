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
import json
import matplotlib.pyplot as plt

file_path = '../PoliceKillingsUS.csv'
data = pd.read_csv(file_path, encoding="Windows-1252")
states = '../state.json'
with open(states, 'r') as js:
    states = json.load(js)

data =data.dropna(how='any')
data['state'] = [states[state] for state in data['state']]
def Region(x):
    if x=='Alabama':
        return('south')
    elif x=='Alaska':
        return('west')
    elif x=='Arizona':
        return('west')
    elif x=='Arkansas':
        return('south')

    elif x=='California':
        return('west')
    
    elif x=='Colorado':
        return('west')
    
    elif x=='Connecticut':
        return('northeast')
    
    elif x == 'District of Columbia':
        return('northeast')
    
    elif x=='Delaware':
        return('south')
    
    elif x=='Florida':
        return('south')
    elif x=='Georgia':
        return('south')
    elif x=='Hawaii':
        return('west')
    elif x=='Idaho':
        return('west')
    elif x=='Illinois':
        return('Midwest')
    elif x=='Indiana':
        return('Midwest')
    elif x=='Iowa':
        return('Midwest')
    elif x=='Kansas':
        return('Midwest')
    elif x=='Kentucky':
        return('south')
    elif x=='Louisiana':
        return('south')
    elif x=='Maine':
        return('northeast')
    elif x=='Maryland':
        return('south')
    elif x=='Massachusetts':
        return('northeast')
    elif x=='Michigan':
        return('Midwest')
    elif x=='Minnesota':
        return('Midwest')
    elif x=='Mississippi':
        return('south')
    elif x=='Missouri':
        return('Midwest')
    elif x=='Montana':
        return('west')
    elif x=='Nebraska':
        return('Midwest')
    elif x=='Nevada':
        return('west')
    elif x=='New Hampshire':
        return('northeast')
    elif x=='New Jersey':
        return('northeast')
    elif x=='New Mexico':
        return('west')
    elif x=='New York':
        return('northeast')
    elif x=='North Carolina':
        return('south')
    elif x=='North Dakota':
        return('Midwest')
    elif x=='Ohio':
        return('Midwest')
    elif x=='Oklahoma':
        return('south')
    elif x=='Oregon':
        return('west')
    elif x=='Pennsylvania':
        return('northeast')
    elif x=='Rhode Island':
        return('northeast')
    elif x=='South Carolina':
        return('south')
    elif x=='South Dakota':
        return('Midwest')
    elif x=='Tennessee':
        return('south')
    elif x=='Texas':
        return('south')
    elif x=='Utah':
        return('west')
    elif x=='Vermont':
        return('northeast')
    elif x=='Virginia':
        return('south')
    elif x=='Washington':
        return('west')
    elif x=='West Virginia':
        return('south')
    elif x=='Wisconsin':
        return('Midwest')
    elif x=='Wyoming':
        return('west')
data['Region']=data['state'].apply(Region)

def count_victims(region, df):
    region_df = df[df['Region'] == region]
    filtered_df = region_df[(region_df['signs_of_mental_illness'] == False)]
    num_victims = filtered_df.shape[0]
    return num_victims

regions = ['south', 'west', 'northeast', 'Midwest']
num_victims = [count_victims(region, data) for region in regions]

plt.bar(regions, num_victims, color=['blue', 'green', 'orange', 'red'])
plt.xlabel('Region')
plt.ylabel('Number of Victims')
plt.title('Number of Victims Killed by Gunshot without Mental Illness by Region')
plt.savefig('./result.png')

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


