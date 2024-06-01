#!/bin/bash

# Input and output file paths
input_file="validation.csv"
output_file="result.csv"

# Create the output file with the header
echo "title,text,subject,date,result" > $output_file

# Read the input file line by line, skipping the header
tail -n +2 $input_file | while IFS=, read -r title text subject date
do
    # Simple heuristic: If 'clickbait' or 'fake news' is in the text, it's fake
    if echo "$text" | grep -q -i 'clickbait\|fake news'; then
        echo "$title,$text,$subject,$date,0" >> $output_file
    else
        echo "$title,$text,$subject,$date,1" >> $output_file
    fi
done
