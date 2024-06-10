import pandas as pd
import matplotlib.pyplot as plt

# Load the dataset
df = pd.read_csv('Amazon Sale Report.csv')

# Filter out rows with cancelled orders
df = df[df['Status'] != 'Cancelled']

# Convert the 'Amount' from INR to USD
exchange_rate = 0.0120988
df['Amount_USD'] = df['Amount'] * exchange_rate

# Convert the 'Amount_USD' to units of $10,000
df['Amount_10K'] = df['Amount_USD'] / 10000

# Aggregate sales by product size
sales_by_size = df.groupby('Size')['Amount_10K'].sum().reset_index()

# Sort the sizes in ascending order
sales_by_size = sales_by_size.sort_values('Size')

# Plotting the bar chart
plt.figure(figsize=(12, 6))
plt.bar(sales_by_size['Size'], sales_by_size['Amount_10K'], color='skyblue')
plt.title('Sales by Product Size')
plt.xlabel('Product Size')
plt.ylabel('Net Revenue in 10,000 dollars')
plt.xticks(rotation=45)
plt.tight_layout()

# Save the plot as a PNG file
plt.savefig('result.png')
