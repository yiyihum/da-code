import pandas as pd
from scipy.stats import f_oneway

# Load the dataset
df = pd.read_csv('yulu_bike_sharing_dataset.csv')

# Group the data by weather conditions and collect the rental counts
grouped = df.groupby('weather')['count'].apply(list)

# Perform ANOVA (Analysis of Variance) to test the hypothesis that two or more groups have the same population mean
anova_results = f_oneway(*grouped)

# Prepare the results to be saved in a CSV file
results_df = pd.DataFrame({
    'Statistic': [anova_results.statistic],
    'P-value': [anova_results.pvalue]
})

# Save the results to 'weather.csv'
results_df.to_csv('weather.csv', index=False)
