import csv

# Define a simple function to score the risk of heart disease
def score_risk(row):
    score = 0
    # Add points for poor general health
    if row['General_Health'] in ['Fair', 'Poor']:
        score += 1
    # Add points for lack of exercise
    if row['Exercise'] == 'No':
        score += 1
    # Add points for existing conditions
    for condition in ['Skin_Cancer', 'Other_Cancer', 'Depression', 'Diabetes', 'Arthritis']:
        if row[condition] == 'Yes':
            score += 1
    # Add points for older age categories (assuming higher risk for older age groups)
    if row['Age_Category'] in ['55-59', '60-64', '65-69', '70-74', '75-79', '80 or older']:
        score += 1
    # Add points for higher BMI
    if float(row['BMI']) >= 30:  # A BMI of 30 or above is considered obese
        score += 1
    # Add points for smoking history
    if row['Smoking_History'] == 'Yes':
        score += 1
    # Add points for poor diet
    if float(row['Fruit_Consumption']) < 30 or float(row['Green_Vegetables_Consumption']) < 30:
        score += 1
    if float(row['Alcohol_Consumption']) > 30 or float(row['FriedPotato_Consumption']) > 30:
        score += 1
    
    # If the score is 3 or more, predict 'Yes' for heart disease, else 'No'
    return 'Yes' if score >= 3 else 'No'

# Read test data
with open('test.csv', mode='r') as csvfile:
    reader = csv.DictReader(csvfile)
    rows = list(reader)

# Predict heart disease for each row in test data
predictions = ['Heart_Disease']
for row in rows:
    prediction = score_risk(row)
    predictions.append(prediction)

# Write the predictions to disease.csv
with open('disease.csv', mode='w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    for prediction in predictions:
        writer.writerow([prediction])