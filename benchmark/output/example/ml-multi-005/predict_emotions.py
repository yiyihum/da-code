from transformers import pipeline

# Load the emotion classification pipeline
classifier = pipeline('text-classification', model='j-hartmann/emotion-english-distilroberta-base')

# Read the test.txt file
with open('test.txt', 'r') as file:
    lines = file.readlines()

# Predict emotions for each line in test.txt
predictions = [classifier(line)[0]['label'] for line in lines]

# Write the predicted emotions to emotions.csv
import csv

with open('emotions.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['emotion'])  # Write the header
    for prediction in predictions:
        writer.writerow([prediction])
