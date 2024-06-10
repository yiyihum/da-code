import matplotlib.pyplot as plt

# The counts of UFO sightings for each country
sightings_count = {'USA': 65114, 'Canada': 3000, 'United Kingdom': 1905, 'Australia': 538, 'Germany': 105}

# Define the colors for each country
colors = ['lightblue', 'gold', 'yellowgreen', 'lightcoral', 'orange']

# Create the bar chart
plt.figure(figsize=(10, 6))
plt.bar(sightings_count.keys(), sightings_count.values(), color=colors)

# Title and labels
plt.title("UFO Sightings by Country")
plt.ylabel("Count")

# Include the countries in the legend
plt.legend(sightings_count.keys())

# Save the chart as result.png
plt.savefig('/workspace/result.png')
plt.close()
