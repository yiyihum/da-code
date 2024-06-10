import pandas as pd
import matplotlib.pyplot as plt

# Load the top 10 neighborhoods data
top_neighborhoods = pd.read_csv('/workspace/top_neighborhoods.csv')

# Create a bar chart
plt.figure(figsize=(16, 8))
plt.bar(top_neighborhoods['neighbourhood'], top_neighborhoods['count'])
plt.title('Top 10 Neighborhoods by Number of Listings')
plt.xlabel('Neighborhood')
plt.ylabel('Number of Listings')
plt.xticks(rotation=45, ha='right')  # Rotate the x-axis labels for better readability

# Save the bar chart as 'result.png'
plt.savefig('/workspace/result.png', bbox_inches='tight')
