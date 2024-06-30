import pandas as pd
import matplotlib.pyplot as plt
import yaml

# Load the stock return data and set 'Date' as the index
returns = pd.read_csv('Big9Returns2017.csv', index_col='Date', parse_dates=True)

# Load the portfolio weights
portfolios = pd.read_csv('EfficientFrontierPortfoliosSlim.csv')

# Calculate equal weights for the equal-weight portfolio
equal_weights = [1/len(returns.columns)] * len(returns.columns)

# Identify the portfolio with the highest Sharpe ratio (assuming risk-free rate is 0)
# Sharpe ratio is calculated as Returns / Volatility
portfolios['SharpeRatio'] = portfolios['Returns'] / portfolios['Volatility']
max_sharpe_idx = portfolios['SharpeRatio'].idxmax()
max_sharpe_portfolio = portfolios.iloc[max_sharpe_idx]

# Extract the weights for the max sharpe ratio portfolio corresponding to the stock tickers
max_sharpe_weights = max_sharpe_portfolio.filter(regex=' weight').values

# Identify the portfolio with the global minimum volatility
min_vol_idx = portfolios['Volatility'].idxmin()
min_vol_portfolio = portfolios.iloc[min_vol_idx]

# Extract the weights for the min volatility portfolio corresponding to the stock tickers
min_vol_weights = min_vol_portfolio.filter(regex=' weight').values

# Calculate the cumulative returns for each portfolio strategy
cumulative_returns = (1 + returns).cumprod()
returns['Cumulative EW'] = cumulative_returns.dot(equal_weights)
returns['Cumulative MSR'] = cumulative_returns.dot(max_sharpe_weights)
returns['Cumulative GMV'] = cumulative_returns.dot(min_vol_weights)

# Load plot specifications from 'plot.yaml'
with open('plot.yaml', 'r') as file:
    plot_specs = yaml.safe_load(file)

# Create the line plot
plt.figure(figsize=plot_specs['figsize'])
plt.plot(returns.index, returns['Cumulative EW'], label=plot_specs['labels'][0])
plt.plot(returns.index, returns['Cumulative MSR'], label=plot_specs['labels'][2])
plt.plot(returns.index, returns['Cumulative GMV'], label=plot_specs['labels'][3])
plt.title(plot_specs['graph_title'])
plt.xlabel(plot_specs['x_label'])
plt.ylabel(plot_specs['y_label'])
plt.legend()
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
    results = [[np.nan if v is None else v for v in result] for result in results]
    results = np.array(results) if results else np.array([])
except Exception as e:
    max_length = max(len(x) for x in results)
    results = [np.pad(x, (0, max_length - len(x)), 'constant') for x in results]

random_string = generate_random_string()
if len(results) > 0:
    npy_path = f'./_data_result_{random_string}.npy'
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

output_path = f'./_result_image_parameters_{random_string}.json'
with open(output_path, 'w') as js:
    json.dump(image_parameters, js)

