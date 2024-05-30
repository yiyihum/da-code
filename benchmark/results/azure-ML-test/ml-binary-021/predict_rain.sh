#!/bin/bash

# Read the test.csv file and predict rain tomorrow based on rain today
# Write the header
echo "RainTomorrow" > tomorrow.csv

# Read the file excluding the header and make predictions
tail -n +2 test.csv | while IFS=, read -r date location minTemp maxTemp rainfall evaporation sunshine windGustDir windGustSpeed windDir9am windDir3pm windSpeed9am windSpeed3pm humidity9am humidity3pm pressure9am pressure3pm cloud9am cloud3pm temp9am temp3pm rainToday
do
  # If it rained today, predict 'Yes' for rain tomorrow, otherwise 'No'
  if [ "$rainToday" == "Yes" ]; then
    echo "Yes" >> tomorrow.csv
  else
    echo "No" >> tomorrow.csv
  fi
done