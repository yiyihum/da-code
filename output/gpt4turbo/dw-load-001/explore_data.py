import pandas as pd

# Load a sample of the Citi Bike trip data
trip_data_sample = pd.read_csv('data/JC-201601-citibike-tripdata.csv', nrows=5)
print("Citi Bike Trip Data Sample:")
print(trip_data_sample)

# Load a sample of the weather data
weather_data_sample = pd.read_csv('data/newark_airport_2016.csv', nrows=5)
print("\nWeather Data Sample:")
print(weather_data_sample)
