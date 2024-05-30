import matplotlib.pyplot as plt
import sys, os, json
from datetime import datetime
import numpy as np
import matplotlib.colors as mcolors
from matplotlib.patches import Wedge, Rectangle
from matplotlib.collections import PathCollection

def identify_plot_type(ax):
    plot_types = set()
    # Check for line plots
    if ax.get_lines():
        return 'line'
    # Check for bar plots
    if ax.patches:
        for patch in ax.patches:
            if isinstance(patch, plt.Rectangle) and patch.get_width() != patch.get_height():
                return 'bar'
    # Check for scatter plots
    if ax.collections:
        for collection in ax.collections:
            if isinstance(collection, plt.PathCollection):
                return 'scatter'
    # Check for pie plots
    if ax.patches:
        for patch in ax.patches:
            if isinstance(patch, plt.Wedge):
                return 'pie'
    return plot_types

import matplotlib.pyplot as plt
import sys, os, json
from datetime import datetime
import numpy as np
import matplotlib.colors as mcolors
from matplotlib.patches import Wedge, Rectangle
from matplotlib.collections import PathCollection

def identify_plot_type(ax):
    plot_types = set()
    # Check for line plots
    if ax.get_lines():
        return 'line'
    # Check for bar plots
    if ax.patches:
        for patch in ax.patches:
            if isinstance(patch, plt.Rectangle) and patch.get_width() != patch.get_height():
                return 'bar'
    # Check for scatter plots
    if ax.collections:
        for collection in ax.collections:
            if isinstance(collection, plt.PathCollection):
                return 'scatter'
    # Check for pie plots
    if ax.patches:
        for patch in ax.patches:
            if isinstance(patch, plt.Wedge):
                return 'pie'
    return plot_types

import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import seaborn as sns

# Read the dataset
df = pd.read_csv('AppleStore.csv')

# Define the categories of interest
categories = ['Education', 'Entertainment', 'Games', 'Others', 'Photo & Video']

# Initialize a dictionary to hold the counts for free and paid apps
category_counts = {category: {'free': 0, 'paid': 0} for category in categories}

# Other category will include all apps not in the predefined categories
other_category = 'Others'

# Process the data
for index, row in df.iterrows():
    category = row['prime_genre']
    if category not in categories:
        category = other_category
    
    if row['price'] == 0.0:
        category_counts[category]['free'] += 1
    else:
        category_counts[category]['paid'] += 1

# Calculate proportions
total_counts = {category: sum(counts.values()) for category, counts in category_counts.items()}
tuple_free = [category_counts[category]['free'] / total_counts[category] for category in categories]
tuple_paidapps = [category_counts[category]['paid'] / total_counts[category] for category in categories]

plt.figure(figsize=(15,8))
N = len(categories)
ind = np.arange(N)    # the x locations for the groups
width = 0.56   # the width of the bars

p1 = plt.bar(ind, tuple_free, width, color='#45cea2')
p2 = plt.bar(ind, tuple_paidapps, width, bottom=tuple_free, color='#fdd470')

plt.xticks(ind, categories)
plt.legend((p1[0], p2[0]), ('Free', 'Paid'))
plt.savefig('./result.png')

image_parameters = {}
ax, fig = plt.gca(), plt.gcf()
gt_graph = identify_plot_type(ax)

results = []
colors = []
if gt_graph == 'bar':
    for patch in ax.patches:
        if isinstance(patch, Rectangle):
            results.append(patch.get_height())
            colors.append(patch.get_facecolor())
    unique_colors = list(set(colors))
    grouped_results = {color: [] for color in unique_colors}
    for height, color in zip(results, colors):
        grouped_results[color].append(height)
    results = [grouped_results[color] for color in grouped_results.keys()]
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

colors = [str(mcolors.to_hex(rgb_tuple)) for rgb_tuple in colors]
figsize = fig.get_size_inches()
legend = ax.get_legend()
title = ax.get_title().get_text() if ax.get_title() else ''
labels = [text.get_text() for text in legend.get_texts()] if legend else []
x_label = ax.get_xlabel().get_text() if ax.get_xlabel() else ''
y_label = ax.get_ylabel().get_text() if ax.get_ylabel() else ''
xtick_labels = [label.get_text() for label in ax.get_xticklabels()]
ytick_labels = [label.get_text() for label in ax.get_yticklabels()]

image_parameters['type'] = gt_graph
image_parameters['color'] = colors
image_parameters['figsize'] = list(figsize)
image_parameters['title'] = title
image_parameters['labels'] = labels
image_parameters['x_label'] = x_label 
image_parameters['y_label'] = y_label
image_parameters['xtick_labels'] = xtick_labels
image_parameters['ytick_labels'] = ytick_labels

output_path = f'./_result_image_parameters_{str(datetime.now())}.json'
with open(output_path, 'w') as js:
    json.dump(image_parameters, js)




image_parameters = {}
ax, fig = plt.gca(), plt.gcf()
gt_graph = identify_plot_type(ax)

results = []
colors = []
if gt_graph == 'bar':
    for patch in ax.patches:
        if isinstance(patch, Rectangle):
            results.append(patch.get_height())
            colors.append(patch.get_facecolor())
    unique_colors = list(set(colors))
    grouped_results = {color: [] for color in unique_colors}
    for height, color in zip(results, colors):
        grouped_results[color].append(height)
    results = [grouped_results[color] for color in grouped_results.keys()]
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

colors = [str(mcolors.to_hex(rgb_tuple)) for rgb_tuple in colors]
figsize = fig.get_size_inches()
legend = ax.get_legend()
title = ax.get_title().get_text() if ax.get_title() else ''
labels = [text.get_text() for text in legend.get_texts()] if legend else []
x_label = ax.get_xlabel().get_text() if ax.get_xlabel() else ''
y_label = ax.get_ylabel().get_text() if ax.get_ylabel() else ''
xtick_labels = [label.get_text() for label in ax.get_xticklabels()]
ytick_labels = [label.get_text() for label in ax.get_yticklabels()]

image_parameters['type'] = gt_graph
image_parameters['color'] = colors
image_parameters['figsize'] = list(figsize)
image_parameters['title'] = title
image_parameters['labels'] = labels
image_parameters['x_label'] = x_label 
image_parameters['y_label'] = y_label
image_parameters['xtick_labels'] = xtick_labels
image_parameters['ytick_labels'] = ytick_labels

output_path = f'./_result_image_parameters_{str(datetime.now())}.json'
with open(output_path, 'w') as js:
    json.dump(image_parameters, js)


