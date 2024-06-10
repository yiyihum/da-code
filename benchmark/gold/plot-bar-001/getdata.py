import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import matplotlib.pyplot as plt # data visualization
import seaborn as sns # statistical data visualization
import warnings # handle warning messages
warnings.filterwarnings('ignore') # Ignore warning messages

df = pd.read_csv('../Song.csv')

# Rename columns to lowercase
df.columns = df.columns.str.lower()

# Rename the 'Radio Plays' column to 'radio_plays'
df.rename(columns={'radio plays': 'radio_plays'}, inplace=True)

# Checking the duplicate values in the data
duplicate_values = df.duplicated().sum()

# List of metrics to plot
metrics = ['sales']  # Add more metrics as needed

# Set the style of seaborn
sns.set_style("whitegrid")
for metric in metrics:
    fig, ax = plt.subplots(figsize=(6, 6))
    
    # Obtain the top ten artists based on the current metric
    top_ten = df.groupby('artist')[metric].agg('mean' if metric == 'rating' else 'sum').nlargest(10).reset_index()
    
    # Plot the top ten artists with vertical bars
    sns.barplot(y='artist', x=metric, data=top_ten, ax=ax, palette='viridis' if metric == 'sales' else 'magma')
    ax.set_title(f'Top Ten Artists Based on {metric.capitalize()}')
    ax.set_ylabel('Artist')
    ax.set_xlabel(f'Total {metric.capitalize()}' if metric == 'sales' else f'Average {metric.capitalize()}')

    plt.xticks(rotation=0)  # Adjust x-axis labels to be horizontal
    plt.tight_layout()
    
    # Save the figure
    fig.savefig(f'{metric}.jpg')


import matplotlib.pyplot as plt
import json
import random, string
import numpy as np
import pprint
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
        
    return ''

def generate_random_string(length=4):
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for _ in range(length))


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
            scatter_data = scatter.get_offsets()
            scatter_data = scatter_data.reshape(-1, 1) if scatter_data.ndim == 1 else scatter_data
            for data in scatter_data:
                results.append(data)
            scatter_colors = scatter.get_facecolor()
            for color in scatter_colors:
                colors.add(tuple(color))

try:
    results = np.array(results) if results else np.array([])
except Exception as e:
    max_length = max(len(x) for x in results)
    results = [np.pad(x, (0, max_length - len(x)), 'constant') for x in results]

random_string = generate_random_string()
if len(results) > 0:
    npy_path = f'./result.npy'
    np.save(npy_path, results)
else:
    npy_path = ''

pprint.pprint(results)
colors = [str(mcolors.to_hex(rgb_tuple)) for rgb_tuple in colors]
fig_size = fig.get_size_inches()
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
image_parameters['figsize'] = list(fig_size)
image_parameters['graph_title'] = graph_title
image_parameters['legend_title'] = legend_title
image_parameters['labels'] = labels
image_parameters['x_label'] = x_label 
image_parameters['y_label'] = y_label
image_parameters['xtick_labels'] = xtick_labels
image_parameters['ytick_labels'] = ytick_labels

output_path = f'./plot.json'
with open(output_path, 'w') as js:
    json.dump(image_parameters, js)

