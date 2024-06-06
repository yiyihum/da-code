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


