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
        
import warnings
# warnings.filterwarnings('ignore')
import os
import re
import math
import glob
import itertools
import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objs as go
import plotly.figure_factory as ff

# Read the csvs
# survey_schema = pd.read_csv(input_dir/ 'SurveySchema.csv')
# freeFormResp = pd.read_csv(input_dir/ 'freeFormResponses.csv')
multiChoiceResp = pd.read_csv('../multipleChoiceResponses.csv')

color = sns.color_palette()

# For REPRODUCIBILITY
seed = 111
np.random.seed(seed)

def pct_on_bars(axs, df, offset=50, orientation='v', adjustment=2, pos='center', prec=1, fontsize=10):
    """
    This function can be used to plot percentage on each bar in a barplot. The function assumes
    that for each value on an axis, there is only one corresponding bar. So, if you have plotted something with
    hue, then you should consider using something else
    
    Arguments:
    axs: Matplotlib axis
    df: pandas dataframe used for this plot
    offset: Relative position of the text w.r.t the bar
    orientation: 'h' or 'v'
    adjustment: If the text overflows the bar on either side, you can adjust it by passing some value
    prec: How much precision is to be used for displaying percentage?
    fontsize: size of the font used in percentage text
    
    """
    
    # Get all the bars
    bars = axs.patches
    
    # Size of dataframe
    items = len(df)
    
    assert round(prec)>-1, "Precision value passed is wrong "
    
    # Iterate over each bar and plot the percentage
    for bar in bars:
        width = bar.get_width()
        height = bar.get_height()
        precision = '{0:.' + str(prec) + '%}'
        
        if math.isnan(width):
            width=0
        if math.isnan(height):
            height=0
        
        # Check orientation of the bars
        if orientation=='h':
            val_to_sub = height/adjustment
            axs.text(width + offset, bar.get_y()+bar.get_height()-val_to_sub, 
                    precision.format(width/items), ha=pos, fontsize=fontsize)
        
        elif orientation=='v':
            val_to_sub = width/adjustment
            axs.text(bar.get_x()+width-val_to_sub, height + offset, 
            precision.format(height/items), ha=pos, fontsize=fontsize)
        
        else:
            print("The orientation value you passed is wrong. It can either be horizontal 'h' or vertical 'v'")

# Select the column for the corresponding question
age_df = multiChoiceResp['Q2'][1:].dropna()
multiChoiceResp_cleanup = multiChoiceResp.dropna(subset=['Q2']).iloc[1:]

order= ['18-21', '22-24', '25-29', '30-34', '35-39', '40-44', '45-49', '50-54', '55-59', '60-69', '70-79', '80+']

f,ax=plt.subplots(figsize=(10,5))

# Do countplot 
ax = sns.countplot(x='Q2', data=multiChoiceResp_cleanup, order=order)

# plot the percentage on bars
pct_on_bars(ax, age_df, orientation='v', offset=50, adjustment=2)

# 删除数据标签
for text in ax.texts:
    text.set_visible(False)

plt.xlabel('Age Group')
plt.ylabel('Count')
plt.title('Age Group Distribution')
plt.savefig('result.png')


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


