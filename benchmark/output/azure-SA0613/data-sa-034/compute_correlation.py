import pandas as pd

# Load the data
data = pd.read_csv('female_literacy_fertility.csv')

# Convert 'female literacy' from percentage to a rate (0 to 1 scale)
data['female_literacy_rate'] = data['female literacy'] / 100

# Calculate the Pearson correlation coefficient between 'female_literacy_rate' and 'fertility'
correlation = data['female_literacy_rate'].corr(data['fertility'])

# Print the correlation coefficient
print("Pearson correlation coefficient:", correlation)

# Save the correlation coefficient to the result.csv file
result = pd.DataFrame({'Pearson correlation coefficient': [correlation]})
result.to_csv('result.csv', index=False)
