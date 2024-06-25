import pandas as pd
import matplotlib.pyplot as plt

# Load the listings data
listings_df = pd.read_csv('listings.csv')

# Count the number of listings in each neighborhood
neighborhood_counts = listings_df['neighbourhood_cleansed'].value_counts()

# Select the top 10 neighborhoods
top_neighborhoods = neighborhood_counts.head(10)

# Create a bar chart
plt.figure(figsize=(16, 8))
top_neighborhoods.plot(kind='bar')
plt.title('Top 10 Neighborhoods by Number of Listings')
plt.xlabel('Neighborhood')
plt.ylabel('Number of Listings')
plt.xticks(rotation=45)
plt.tight_layout()

# Save the bar chart as 'result.png'
plt.savefig('result.png')
