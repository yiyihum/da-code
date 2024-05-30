#!/bin/bash

# Prediction function
predict_news() {
    local title="$1"
    if grep -qiw "reuters" <<< "$title"; then
        echo "1"
    else
        echo "0"
    fi
}

# Header for result.csv
echo "result" > result.csv

# Read validation.csv line by line, skip the header
tail -n +2 validation.csv | while IFS=, read -r index title rest; do
    # Predict news and append to result.csv
    result=$(predict_news "$title")
    echo "$result" >> result.csv
done