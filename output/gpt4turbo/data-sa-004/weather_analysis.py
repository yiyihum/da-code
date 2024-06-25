import pandas as pd
from scipy.stats import f_oneway

# Load the dataset
df = pd.read_csv('yulu_bike_sharing_dataset.csv')

# Group the data by 'weather' and calculate the sum of bike rentals for each weather condition
grouped_data = df.groupby('weather')['count'].sum().reset_index()

# Perform ANOVA (Analysis of Variance) to test the hypothesis that there are differences
# between the means of bike rentals across different weather conditions
anova_results = f_oneway(*[group['count'] for name, group in df.groupby('weather')])

# Prepare the grouped data results to be saved in a CSV file
grouped_data_df = pd.DataFrame({
    'Weather_Condition': grouped_data['weather'],
    'Total_Rentals': grouped_data['count'],
    # Repeat the ANOVA results for each weather condition
    'ANOVA_F': [anova_results.statistic] * len(grouped_data),
    'ANOVA_p': [anova_results.pvalue] * len(grouped_data)
})

# Save the results to 'weather.csv'
grouped_data_df.to_csv('weather.csv', index=False)
