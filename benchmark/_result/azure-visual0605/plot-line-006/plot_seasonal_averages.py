import pandas as pd
import matplotlib.pyplot as plt

# Load the dataset
df = pd.read_csv('GlobalTemperatures.csv', parse_dates=['dt'])

# Filter out the unnecessary columns
df = df[['dt', 'LandAverageTemperature']]

# Exclude the data from the specified regions (not applicable for this file)

# Define the seasons based on the month
def get_season(month):
    if month in [3, 4, 5]:
        return 'Spring'
    elif month in [6, 7, 8]:
        return 'Summer'
    elif month in [9, 10, 11]:
        return 'Autumn'
    elif month in [12, 1, 2]:
        return 'Winter'

# Apply the function to get the season for each row
df['Season'] = df['dt'].dt.month.apply(get_season)

# Group by year and season, then calculate the mean temperature
seasonal_avg = df.groupby([df['dt'].dt.year, 'Season'])['LandAverageTemperature'].mean().unstack()

# Plotting
plt.figure(figsize=(16, 6))
seasonal_avg.plot(title='Average temperature in each season', color={"Spring": "#ffa500", "Summer": "#0000ff", "Autumn": "#008000", "Winter": "#ff0000"})
plt.xlabel('Year')
plt.ylabel('Average temperature')
plt.legend(title='Seasons Average Temperature', labels=['Spring', 'Summer', 'Autumn', 'Winter'])
plt.savefig('result.png')
