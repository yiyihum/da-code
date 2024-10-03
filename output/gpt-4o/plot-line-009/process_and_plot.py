import pandas as pd
import matplotlib.pyplot as plt
import yaml

# Load the dataset
df = pd.read_csv('city_temperature.csv', dtype={'State': str})

# Filter for Karachi and Islamabad
df = df[(df['City'] == 'Karachi') | (df['City'] == 'Islamabad')]

# Filter for the years 1995 to 2019
df = df[(df['Year'] >= 1995) & (df['Year'] <= 2019)]

# Convert Fahrenheit to Celsius
df['AvgTemperatureC'] = (df['AvgTemperature'] - 32) * 5.0/9.0

# Filter out records with AvgTemperatureC less than -70
df = df[df['AvgTemperatureC'] >= -70]

# Load plot formatting details from plot.yaml
with open('plot.yaml', 'r') as file:
    plot_config = yaml.safe_load(file)

# Prepare data for plotting
karachi = df[df['City'] == 'Karachi'].groupby('Year')['AvgTemperatureC'].mean()
islamabad = df[df['City'] == 'Islamabad'].groupby('Year')['AvgTemperatureC'].mean()

# Generate x-tick labels dynamically based on the years present in the data
years = sorted(df['Year'].unique())
xtick_labels = [str(year) for year in years]

# Plot the data
plt.figure(figsize=plot_config['figsize'])
plt.plot(karachi.index, karachi.values, label=plot_config['labels'][0], color=plot_config['color'][0])
plt.plot(islamabad.index, islamabad.values, label=plot_config['labels'][1], color=plot_config['color'][1])
plt.title(plot_config['graph_title'])
plt.xlabel(plot_config['x_label'])
plt.ylabel(plot_config['y_label'])
plt.xticks(ticks=years, labels=xtick_labels, rotation=45)
plt.legend()
plt.grid(True)
plt.tight_layout()

# Save the plot
plt.savefig('result.png')
plt.close()
