#!/bin/bash

# Read from the test.csv file, skip the header, and then use awk to map "Yes" to "Positive" and "No" to "Negative"
tail -n +2 test.csv | awk -F ',' '{print ($11=="Yes"?"Positive":"Negative")}' > temp_results.csv

# Add the header "Sentiment" to the result.csv file
echo "Sentiment" > result.csv

# Append the temp_results.csv content to result.csv
cat temp_results.csv >> result.csv

# Remove the temporary file
rm temp_results.csv