import pandas as pd
import matplotlib.pyplot as plt

# Assuming the CSV data is saved in a file called 'bicycle_sales.csv'
df = pd.read_csv('Kaggle3-2_0//gold//result.csv')

# Pivot the DataFrame to make months the index, categories the columns, and values the average units sold
pivot_df = df.pivot(index='month', columns='category_name', values='avg_units_sold')

# Plotting the data
pivot_df.plot(figsize=(14, 8), marker='o')

# Enhancing the plot with titles and labels
plt.title('Average Units Sold per Month for Each Bicycle Category')
plt.xlabel('Month')
plt.ylabel('Average Units Sold')
plt.grid(True)
plt.legend(title='Category', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()

# Display the plot
plt.show()