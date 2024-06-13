# Open the file and print the first 10 lines to inspect its structure
with open('sheffield_weather_station.csv', 'r') as file:
    for _ in range(10):
        print(file.readline())
