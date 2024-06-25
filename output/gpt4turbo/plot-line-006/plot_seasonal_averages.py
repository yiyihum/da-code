import pandas as pd
import matplotlib.pyplot as plt

# Load the seasonal average temperatures data
seasonal_avg_pivot = pd.read_csv('/workspace/seasonal_average_temperatures.csv')

# Drop rows with NaN values as they represent years with incomplete data for some seasons
seasonal_avg_pivot.dropna(inplace=True)

# Plotting the graph
plt.figure(figsize=(16, 6))
plt.plot(seasonal_avg_pivot['dt'], seasonal_avg_pivot['Spring'], label='Spring', color='#ffa500')
plt.plot(seasonal_avg_pivot['dt'], seasonal_avg_pivot['Summer'], label='Summer', color='#0000ff')
plt.plot(seasonal_avg_pivot['dt'], seasonal_avg_pivot['Autumn'], label='Autumn', color='#008000')
plt.plot(seasonal_avg_pivot['dt'], seasonal_avg_pivot['Winter'], label='Winter', color='#ff0000')

# Adding title and labels
plt.title('Average temperature in each season')
plt.xlabel('Year')
plt.ylabel('Average temperature')

# Adding legend
plt.legend(title='Seasons Average Temperature')

# Save the figure
plt.savefig('/workspace/result.png')

# Display the plot
plt.show()
