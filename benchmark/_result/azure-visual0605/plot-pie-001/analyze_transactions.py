import pandas as pd
import matplotlib.pyplot as plt

# Load the dataset
df = pd.read_csv('/workspace/MyTransaction.csv')

# Count the number of transactions in each category
category_counts = df['Category'].value_counts()

# Get the top four categories
top_categories = category_counts.head(4)

# Plot a pie chart for the top four categories
plt.figure(figsize=(8, 6))
top_categories.plot(kind='pie', autopct='%1.1f%%')
plt.title('Top Four Categories by Number of Transactions')
plt.ylabel('')  # Hide the y-label

# Save the pie chart as an image
plt.savefig('/workspace/answer.png')
