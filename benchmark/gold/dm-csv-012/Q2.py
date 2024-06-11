import pandas as pd

# Load the dataset that contains the sales data
sales_data = pd.read_csv('result.csv')

# Calculate total sales
total_sales = sales_data['total_spent'].sum()

# Calculate and sort customers by their sales in descending order
sorted_sales = sales_data.sort_values(by='total_spent', ascending=False)

# Determine the number of top customers to represent the top 20%
num_top_customers = int(len(sorted_sales) * 0.2)

# Calculate the sales of the top 20% customers
top_customers_sales = sorted_sales.head(num_top_customers)['total_spent'].sum()

# Calculate the percentage of total sales
percentage_of_total_sales = (top_customers_sales / total_sales) * 100

# Print results
print(f"Total Sales: {total_sales}")
print(f"Sales from Top 20% Customers: {top_customers_sales}")
print(f"Top 20% of customers account for {percentage_of_total_sales:.2f}% of total sales.")

# Check if the Pareto Principle applies
if percentage_of_total_sales >= 80:
    print("The Pareto Principle applies: the top 20% of customers are responsible for 80% or more of total sales.")
else:
    print("The Pareto Principle does not apply: the top 20% of customers are responsible for less than 80% of total sales.")