import pandas as pd

# Load the data from the CSV file
data = pd.read_csv('monthly_deaths.csv')

# Convert the 'date' column to datetime
data['date'] = pd.to_datetime(data['date'])

# Split the data into before and after handwashing started
handwashing_start = pd.to_datetime('1847-06-01')
before_handwashing = data[data['date'] < handwashing_start]
after_handwashing = data[data['date'] >= handwashing_start]

# Calculate the monthly proportion of deaths before and after handwashing
before_handwashing['proportion'] = before_handwashing['deaths'] / before_handwashing['births']
after_handwashing['proportion'] = after_handwashing['deaths'] / after_handwashing['births']

# Calculate the average reduction in the monthly proportion of deaths
average_reduction = before_handwashing['proportion'].mean() - after_handwashing['proportion'].mean()

# Output the result
print(average_reduction)
