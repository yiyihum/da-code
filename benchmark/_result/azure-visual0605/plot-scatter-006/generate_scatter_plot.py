import pandas as pd
import matplotlib.pyplot as plt

# Load the dataset
df = pd.read_csv('/workspace/Books_df.csv')

# Extract the 'Price' and 'Rating' columns
prices = df['Price']
ratings = df['Rating']

# Create a scatter plot
plt.figure(figsize=(12, 8))
plt.scatter(ratings, prices, color='blue', alpha=0.5)

# Set the y-axis to a logarithmic scale
plt.yscale('log')

# Set the title and labels
plt.title('Price vs. Rating of Books')
plt.xlabel('Rating')
plt.ylabel('Price')

# Save the plot as 'result.jpg'
plt.savefig('/workspace/result.jpg')
