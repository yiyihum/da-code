import pandas as pd
import matplotlib.pyplot as plt

# Load the filtered dataset with low_memory=False to handle mixed types
df = pd.read_csv('/workspace/filtered_temperature.csv', low_memory=False)

# Ensure 'Year' is treated as an integer
df['Year'] = df['Year'].astype(int)

# Filter for Karachi and Islamabad between 1995 and 2019
cities = ['Karachi', 'Islamabad']
df_cities = df[(df['City'].isin(cities)) & (df['Year'] >= 1995) & (df['Year'] <= 2019)]

# Group by City and Year to calculate the average temperature for each year
df_avg_temp = df_cities.groupby(['City', 'Year'])['AvgTemperatureC'].mean().reset_index()

# Plotting
plt.figure(figsize=(12, 8))
for city in cities:
    city_data = df_avg_temp[df_avg_temp['City'] == city]
    plt.plot(city_data['Year'], city_data['AvgTemperatureC'], label=city, marker='o')

# Formatting the plot
plt.title('Average Temperature Comparison between Karachi and Islamabad')
plt.xlabel('Year')
plt.ylabel('AvgTemperature (°C)')
plt.legend()
plt.grid(True)

# Save the plot as a PNG file
plt.savefig('/workspace/result.png')
