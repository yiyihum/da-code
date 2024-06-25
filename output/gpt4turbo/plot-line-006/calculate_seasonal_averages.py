import pandas as pd

# Load the dataset
df = pd.read_csv('/workspace/GlobalTemperatures.csv')

# Convert the 'dt' column to datetime
df['dt'] = pd.to_datetime(df['dt'])

# Define the seasons based on the month
def get_season(month):
    if month in [3, 4, 5]:
        return 'Spring'
    elif month in [6, 7, 8]:
        return 'Summer'
    elif month in [9, 10, 11]:
        return 'Autumn'
    else:
        # December, January, February
        return 'Winter'

# Apply the function to get the season for each row
df['Season'] = df['dt'].dt.month.apply(get_season)

# Group by year and season, then calculate the mean temperature
seasonal_avg = df.groupby([df['dt'].dt.year, 'Season'])['LandAndOceanAverageTemperature'].mean().reset_index()

# Pivot the table to have seasons as columns and years as rows
seasonal_avg_pivot = seasonal_avg.pivot(index='dt', columns='Season', values='LandAndOceanAverageTemperature')

# Save the pivoted data to a CSV for further analysis
seasonal_avg_pivot.to_csv('/workspace/seasonal_average_temperatures.csv', index=True)

print(seasonal_avg_pivot.head())
