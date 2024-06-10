import pandas as pd
import matplotlib.pyplot as plt

# Load the dataset
books_df = pd.read_csv('Books_df.csv')

# Calculate the average price per author
average_prices = books_df.groupby('Author')['Price'].mean().sort_values(ascending=False).head(10)

# Create a bar chart
plt.figure(figsize=(18, 12))
average_prices.plot(kind='barh')
plt.xlabel('Average Price')
plt.ylabel('Author')
plt.title('Most Expensive Author')
plt.gca().invert_yaxis()  # To display the highest price at the top
plt.savefig('result.jpg')
