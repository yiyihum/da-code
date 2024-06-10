import numpy as np 
import pandas as pd 
import seaborn as sns
import matplotlib.pyplot as plt

import plotly
import plotly.express as px
import plotly.graph_objs as gobj
from plotly.offline import download_plotlyjs,init_notebook_mode,plot,iplot
from collections import Counter

import statsmodels.api as sm
import scipy.stats.distributions as dist
from scipy.stats import t,ttest_rel
from statsmodels.stats.weightstats import ztest

from warnings import simplefilter
simplefilter("ignore")

data15 = pd.read_csv('../2015.csv');  
data16 = pd.read_csv('../2016.csv');  
data17 = pd.read_csv('../2017.csv');  
data18 = pd.read_csv('../2018.csv');  
data19 = pd.read_csv('../2019.csv');  

collection = [data15,data16,data17,data18,data19]

# Naming the datasets
data15.name = 'data15'
data16.name = 'data16'
data17.name = 'data17'
data18.name = 'data18'
data19.name = 'data19'

data_scores = pd.DataFrame()
DS = pd.DataFrame()

data_scores[['country','region','2015_rank','2015_score']] = data15[['Country','Region','Happiness Rank','Happiness Score']]

d16 = pd.DataFrame()
d17 = pd.DataFrame()
d18 = pd.DataFrame()
d19 = pd.DataFrame()

d16[['country','2016_rank','2016_score']] = data16[['Country','Happiness Rank','Happiness Score']]
d17[['country','2017_rank','2017_score']] = data17[['Country','Happiness.Rank','Happiness.Score']]
d18[['country','2018_rank','2018_score']] = data18[['Country or region','Overall rank','Score']]
d19[['country','2019_rank','2019_score']] = data19[['Country or region','Overall rank','Score']]
data_scores = data_scores.merge(d16,on=['country'])
data_scores = data_scores.merge(d17,on=['country'])
data_scores = data_scores.merge(d18,on=['country'])
data_scores = data_scores.merge(d19,on=['country'])

x = [2015,2016,2017,2018,2019]
y1 = [7.285000,7.323500,7.299000,7.298000,7.267500]
y2 = [7.273000,7.254000,7.154500,7.107000,7.085000]
y3 = [6.739350,6.731400,6.748400,6.829100,6.898400]
y4 = [6.137300,6.050500,5.947400,5.937750,5.942550]
y5 = [5.496250,5.477000,5.496500,5.540250,5.564250]
y6 = [5.372625,5.396750,5.444875,5.399750,5.333375]
y7 = [5.344571,5.379607,5.418321,5.473929,5.571786]
y8 = [5.330789,5.386053,5.369684,5.282737,5.237000]
y9 = [4.580857,4.563286,4.628429,4.603857,4.526857]
y10 = [4.120419,4.074839,4.131129,4.247968,4.380323]

plt.figure(figsize=(12,6))
plt.plot(x, y1, '-o', label='ANZ')  # Australia and New Zealand
plt.plot(x, y2, '-o', label='NA')   # North America
plt.plot(x, y3, '-o', label='WEU')  # Western Europe
plt.plot(x, y4, '-o', label='LAC')  # Latin America and Caribbean
plt.plot(x, y5, '-o', label='EA')   # Eastern Asia
plt.plot(x, y6, '-o', label='SEA')  # Southeastern Asia
plt.plot(x, y7, '-o', label='CEE')  # Central and Eastern Europe
plt.plot(x, y8, '-o', label='MENA') # Middle East and Northern Africa
plt.plot(x, y9, '-o', label='SA')   # Southern Asia
plt.plot(x, y10, '-o', label='SSA') # Sub-Saharan Africa


plt.title('Happiness Scores in 2015-2019')
plt.xticks(fontsize=14)
plt.legend(loc='upper left',fontsize=8);


import matplotlib.pyplot as plt
import json
import random, string
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

output_path = f'./plot.json'
with open(output_path, 'w') as js:
    json.dump(image_parameters, js)

