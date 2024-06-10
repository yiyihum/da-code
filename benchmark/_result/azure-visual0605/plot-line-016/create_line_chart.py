import pandas as pd
import matplotlib.pyplot as plt

# Load the dataset
df = pd.read_csv('museum_visitors.csv', parse_dates=['Date'])

# Set the figure size
plt.figure(figsize=(14, 6))

# Plot the line chart for Avila Adobe visitors
plt.plot(df['Date'], df['Avila Adobe'], label='Avila Adobe', color='blue')

# Set the title and labels
plt.title('Number of visitors to Avila Adobe Museum from 2014 to 2019')
plt.xlabel('Date')
plt.ylabel('Avila Adobe')

# Add the legend
plt.legend()

# Save the plot as a PNG file
plt.savefig('result.png')
