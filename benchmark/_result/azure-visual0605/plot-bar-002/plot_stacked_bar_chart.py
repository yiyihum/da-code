import pandas as pd
import matplotlib.pyplot as plt

# Load the data
df = pd.read_csv('/workspace/data.csv')

# Clean and prepare the data
# Remove rows with missing or invalid ratings
df = df[df['rate'].notnull() & df['rate'].str.contains('/')]
# Extract the rating and convert it to a float
df['rating'] = df['rate'].apply(lambda x: float(x.split('/')[0]) if x != 'NEW' and x != '-' else None)
df.dropna(subset=['rating'], inplace=True)

# Group by rating and online_order status
grouped = df.groupby(['rating', 'online_order']).size().unstack(fill_value=0)

# Calculate the percentage of online orders for each rating
grouped_percentage = grouped.div(grouped.sum(axis=1), axis=0) * 100

# Plot the stacked bar chart
ax = grouped_percentage.plot(kind='bar', stacked=True, figsize=(10, 7), colormap='viridis')
plt.title("Percentage of Restaurants' Online Order Option by Rating")
plt.xlabel('Rating')
plt.ylabel('Percentage of Online Orders')
plt.legend(title='Online Order', labels=['No', 'Yes'])

# Save the plot as an image file
plt.savefig('/workspace/result.jpg', format='jpg', bbox_inches='tight')
plt.close()
