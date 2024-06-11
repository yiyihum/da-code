import pandas as pd

# Load the data from the CSV file
data = pd.read_csv('Kaggle7-1_1\\marketing_data.csv')

# Create age groups
data['Age'] = 2024 - data['Year_Birth']
data['Age_Group'] = pd.cut(data['Age'], bins=[0, 20, 30, 40, 50, 60, 70, 80, 90, 100])

# Drop rows with missing values
data.dropna(subset=['Age_Group', 'Country'], inplace=True)

# Calculate the mean response rate for each combination of Age_Group and Country
age_country_response_mean = data.groupby(['Age_Group', 'Country'])['Response'].mean().reset_index()
age_country_response_mean.dropna(subset=['Response'], inplace=True)

# Save the results to result.csv
age_country_response_mean.to_csv('Kaggle7-1_1\\gold\\result.csv', index=False)

print("Results saved to result.csv.")