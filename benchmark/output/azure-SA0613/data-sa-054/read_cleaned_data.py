import pandas as pd

# Read the CSV file, skipping initial lines with comments and specifying the delimiter
data = pd.read_csv('sheffield_weather_station.csv', comment='#', delim_whitespace=True)

# Display the first few rows of the dataframe to confirm correct parsing
print(data.head())
