import pandas as pd
import matplotlib.pyplot as plt

# Load the dataset
df = pd.read_csv('/workspace/MyTransaction.csv')

# Count the number of transactions per category
category_counts = df['Category'].value_counts()

# Select the top 4 categories
top_categories = category_counts.head(4)

# Create a pie chart
plt.figure(figsize=(8, 6))
top_categories.plot.pie(autopct='%1.1f%%', startangle=90)
plt.title('Transaction Distribution by Category')
plt.ylabel('')  # Hide the y-label

# Save the pie chart as an image
plt.savefig('/workspace/result.jpg')
