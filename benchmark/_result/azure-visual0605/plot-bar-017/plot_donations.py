import pandas as pd
import matplotlib.pyplot as plt

# Read the data from CSV
df = pd.read_csv('party_sums.csv')

# Sort the dataframe by total donations in descending order
df_sorted = df.sort_values(by='Total_Denominations', ascending=False)

# Create the bar chart
plt.figure(figsize=(14, 8))
plt.barh(df_sorted['Political_party_Name'], df_sorted['Total_Denominations'])
plt.xlabel('Total Denominations')
plt.ylabel('Political Party')
plt.title('Total Denominations by Political Party')

# Save the plot as a PNG file
plt.savefig('party_sums_plot.png')
