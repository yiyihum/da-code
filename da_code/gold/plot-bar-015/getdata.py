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
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# Load the dataset
amazon = pd.read_csv('../Amazon Sale Report.csv', low_memory=False)

# Display count of unique values in each column
amazon.nunique().to_frame(name='Count of unique values')

# Drop unnecessary columns
amazon.drop(columns=['index', 'Unnamed: 22', 'fulfilled-by', 'ship-country', 'currency', 'Sales Channel '], inplace=True)

# Remove duplicates
amazon.drop_duplicates(subset=['Order ID', 'ASIN'], inplace=True, ignore_index=True)
# Fill missing values
amazon['Courier Status'] = amazon['Courier Status'].fillna('unknown')
amazon['promotion-ids'] = amazon['promotion-ids'].fillna('no promotion')

# Check the 'Amount' column for missing values based on 'Status'
print(amazon[amazon['Amount'].isnull()]['Status'].value_counts(normalize=True).apply(lambda x: format(x, '.2%')))

# Fill missing 'Amount' with 0
amazon['Amount'] = amazon['Amount'].fillna(0)

# Fill missing shipping information
amazon['ship-city'] = amazon['ship-city'].fillna('unknown')
amazon['ship-state'] = amazon['ship-state'].fillna('unknown')
amazon['ship-postal-code'] = amazon['ship-postal-code'].fillna('unknown')

# Rename columns
mapper = {
    'Order ID': 'order_ID', 'Date': 'date', 'Status': 'ship_status', 'Fulfilment': 'fullfilment',
    'ship-service-level': 'service_level', 'Style': 'style', 'SKU': 'sku', 'Category': 'product_category',
    'Size': 'size', 'ASIN': 'asin', 'Courier Status': 'courier_ship_status', 'Qty': 'order_quantity',
    'Amount': 'order_amount_($)', 'ship-city': 'city', 'ship-state': 'state', 'ship-postal-code': 'zip',
    'promotion-ids': 'promotion', 'B2B': 'customer_type'
}
amazon.rename(columns=mapper, inplace=True)

# Convert INR to USD using an exchange rate of 1 INR = 0.0120988 USD
exchange_rate = 0.0120988
amazon['order_amount_($)'] = amazon['order_amount_($)'].apply(lambda x: x * exchange_rate)

# Replace True/False in 'customer_type' with 'business'/'customer'
amazon['customer_type'] = amazon['customer_type'].replace({True: 'business', False: 'customer'})

# Convert 'date' to datetime
amazon['date'] = pd.to_datetime(amazon['date'], infer_datetime_format=True)

# Filter out March dates and remove them from the dataset
march_dates = amazon['date'][amazon['date'].dt.month == 3]
amazon = amazon[amazon['date'].dt.month != 3]

# Add a 'month' column
amazon['month'] = amazon['date'].dt.month
month_map = {4: 'april', 5: 'may', 6: 'june'}
amazon['month'] = amazon['month'].map(month_map)

# Define the desired order of months
month_order = ['april', 'may', 'june']
amazon['month'] = pd.Categorical(amazon['month'], categories=month_order, ordered=True)

# Define the desired order of sizes
size_order = ['Free', 'XS', 'S', 'M', 'L', 'XL', 'XXL', '3XL', '4XL', '5XL', '6XL']
amazon['size'] = pd.Categorical(amazon['size'], categories=size_order, ordered=True)

# Group the data by product size and calculate the total sales
sales_by_size = amazon.groupby('size')['order_amount_($)'].sum()

# Create a horizontal bar chart to show the sales by product size
fig, ax = plt.subplots(figsize=(12, 6))

# Use a color palette to highlight specific sizes
sns.barplot(x=sales_by_size.index, y=sales_by_size.values, ax=ax)

# Set font sizes for x and y labels, title, and ticks
ax.set_xlabel('Product Size', labelpad=3, fontsize=14)
ax.set_ylabel('Net Revenue in 10,000 dollars', labelpad=3, fontsize=14)
ax.set_title('Sales by Product Size', fontsize=20, x=0.085, y=1.05, pad=10)

# Set the y-axis ticks and labels
num_y_ticks = 10
y_tick_values = np.linspace(0, sales_by_size.max(), num_y_ticks)
ax.set_yticks(y_tick_values)
ax.set_yticklabels([f'{int(val/10000)}' for val in y_tick_values])

# Add gridlines and style the plot
# ax.yaxis.grid(linestyle='--', color='gray', linewidth=0.5, dashes=(8, 5))
ax.xaxis.grid(False)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_visible(False)
ax.spines['bottom'].set_linewidth(2)
ax.spines['bottom'].set_color('black')
ax.tick_params(axis='both', labelsize=12)

# Save the plot as a PNG file
fig.savefig('./result.png')




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


