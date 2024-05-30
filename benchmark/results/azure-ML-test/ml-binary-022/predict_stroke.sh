#!/bin/bash

# This script predicts stroke based on simple heuristic rules.

INPUT_FILE="test.csv"
OUTPUT_FILE="stroke.csv"
DELIMITER=","

# Create the output file and write the header
echo "stroke" > $OUTPUT_FILE

# Read the input file, skip the header, and process lines one by one
tail -n +2 $INPUT_FILE | while IFS=$DELIMITER read -r id gender age hypertension heart_disease ever_married work_type Residence_type avg_glucose_level bmi smoking_status
do
    # Convert age to an integer by removing the decimal part
    age_int=$(echo $age | cut -d'.' -f1)

    # Apply simple rules to predict stroke
    stroke_prediction=0
    if [ "$age_int" -gt 50 ] || [ "$hypertension" -eq 1 ] || [ "$heart_disease" -eq 1 ]; then
        stroke_prediction=1
    fi

    # Write the prediction to the output file
    echo $stroke_prediction >> $OUTPUT_FILE
done