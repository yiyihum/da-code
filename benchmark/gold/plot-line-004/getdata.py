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
        if isinstance(collection, PathCollection):
            return 'scatter'

    # Check for line plots
    lines = ax.get_lines()
    for line in lines:
        if len(line.get_xdata()) > 1 and len(line.get_ydata()) > 1:
            return 'line'
        
import sqlite3  # For connecting to SQLite database
import pandas as pd  # For data manipulation and analysis
import numpy as np  # For numerical operations
from sklearn.model_selection import train_test_split  # For splitting data into training and testing sets
from sklearn.ensemble import RandomForestClassifier  # For building a Random Forest classifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix  # For evaluating model performance
import matplotlib.pyplot as plt  # For data visualization
import seaborn as sns  # For enhanced data visualization

# Additional libraries for data manipulation and visualization
from sklearn.preprocessing import StandardScaler  # For feature scaling
from sklearn.metrics import roc_auc_score, roc_curve  # For ROC curve analysis
from sklearn.model_selection import cross_val_score, GridSearchCV  # For hyperparameter tuning
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.linear_model import LinearRegression

db_path = '../olist.sqlite'
db_connection = sqlite3.connect(db_path)

def execute_query(query):
    return pd.read_sql_query(query, db_connection)

# Explore tables in the database
tables_query = "SELECT name FROM sqlite_master WHERE type='table';"
tables = execute_query(tables_query)

# Display tables in a structured format
print("Tables in the database:")
print(tables)



# Query to get the count of orders for each order status over time
order_status_time_query = """
SELECT strftime('%Y-%m', order_purchase_timestamp) AS month, 
       order_status, 
       COUNT(*) AS count
FROM orders
GROUP BY strftime('%Y-%m', order_purchase_timestamp), order_status
ORDER BY month;
"""

# Execute query and fetch data
order_status_time_data = execute_query(order_status_time_query)

# Plotting the trend of order statuses over time
plt.figure(figsize=(18, 6))
sns.lineplot(x='month', y='count', hue='order_status', data=order_status_time_data)
plt.title('Trend of Order Statuses Over Time')
plt.xlabel('Month')
plt.grid(False)
plt.ylabel('Order Count')
plt.xticks(rotation=45)
plt.legend(title='Order Status')
plt.savefig('result.png')


image_parameters = {}
ax, fig = plt.gca(), plt.gcf()
gt_graph = identify_plot_type(ax)
print(gt_graph)
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
        if len(line.get_xdata()) > 1 and len(line.get_ydata()) > 1:
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


max_length = max(len(x) for x in results)
results = [np.pad(x, (0, max_length - len(x)), 'constant') for x in results]

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


