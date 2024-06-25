import pandas as pd
import matplotlib.pyplot as plt

# Load the sales data
sales_data = pd.read_csv('Sale Report.csv')

# Group the data by 'Size' and sum up the 'Stock' values
sales_by_size = sales_data.groupby('Size')['Stock'].sum().reset_index()

# Convert the 'Stock' values to units of $10,000
sales_by_size['Stock'] = sales_by_size['Stock'] / 10000

# Sort the sizes in ascending order
sales_by_size.sort_values('Size', inplace=True)

# Plot the figures in a bar chart
plt.figure(figsize=(12, 6))
plt.bar(sales_by_size['Size'], sales_by_size['Stock'])
plt.title('Sales by Product Size')
plt.xlabel('Product Size')
plt.ylabel('Net Revenue in 10,000 dollars')
plt.savefig('result.png')

# Display the plot
plt.show()
