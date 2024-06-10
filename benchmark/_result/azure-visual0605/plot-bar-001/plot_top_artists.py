import pandas as pd
import matplotlib.pyplot as plt

# Load the dataset
df = pd.read_csv('/workspace/Song.csv')

# Group by artist and sum the sales
artist_sales = df.groupby('Artist')['Sales'].sum().sort_values(ascending=False).head(10)

# Plot the top ten artists based on sales
plt.figure(figsize=(6, 6))
artist_sales.plot(kind='barh', color='skyblue')
plt.title('Top Ten Artists Based on Sales')
plt.xlabel('Total Sales')
plt.ylabel('Artist')
plt.gca().invert_yaxis()  # To display the highest sales at the top
plt.tight_layout()

# Save the plot as an image file
plt.savefig('/workspace/sales.jpg')
