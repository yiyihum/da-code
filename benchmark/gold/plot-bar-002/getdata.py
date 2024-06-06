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
        
import numpy as np  # Linear algebra library for Python.
import pandas as pd  # Data processing library, particularly useful for handling CSV files.
import matplotlib.pyplot as plt  # Library for creating static, animated, and interactive visualizations in Python.
import seaborn as sns  # Statistical data visualization library based on matplotlib.
import sqlite3  # Library to interact with SQLite database.

# Connect to the Zomato SQLite database.
con = sqlite3.connect('../zomato_rawdata.sqlite')
# Read the 'Users' table into a DataFrame.
df = pd.read_sql_query("SELECT * FROM Users", con)

# Display the number of missing values in each column.
number_of_missing_values = df.isnull().sum()
# Calculate the percentage of missing values for each column.
percentage_of_missing_values = df.isnull().sum() / len(df) * 100
# List all unique values in the 'rate' column.
unique_rate_values = df['rate'].unique()
# Replace 'NEW' and '-' with NaN (Not a Number) in the 'rate' column.
df['rate'].replace(('NEW', '-'), np.nan, inplace=True)
# Verify that the values were replaced by checking the unique values in 'rate' again.
unique_rate_values_post_replacement = df['rate'].unique()

# Convert the 'rate' column to a float, ignoring any entries that are not strings.
df['rate'] = df['rate'].apply(lambda x: float(x.split('/')[0]) if isinstance(x, str) else x)

# Create a crosstab of ratings against online order presence.
x = pd.crosstab(df['rate'], df['online_order'])

# Normalize the crosstab by dividing by the sum along rows and multiply by 100 to get percentages.
normalize_df = x.div(x.sum(axis=1).astype(float), axis=0)
# Plot the normalized crosstab as a stacked bar chart.
(normalize_df * 100).plot(kind='bar', stacked=True)

# Show the plot.
plt.title('Percentage of Restaurants\' Online Order Option by Rating')
plt.xlabel('Rating')
plt.ylabel('Percentage of Online Orders')

# Save the figure to a JPG file named 'online_order_percentage_by_rating.jpg'.
plt.savefig('./result.jpg')

# Show the plot.
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
            results.append(scatter.get_offsets().data)
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
    npy_path = f'./_data_result_{random_string}.npy'
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

output_path = f'./_result_image_parameters_{random_string}.json'
with open(output_path, 'w') as js:
    json.dump(image_parameters, js)


