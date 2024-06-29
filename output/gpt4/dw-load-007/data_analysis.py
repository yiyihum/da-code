import pandas as pd

# Load the datasets
fortune_df = pd.read_csv('fortune.csv')
stackoverflow_df = pd.read_csv('stackoverflow.csv')

# Calculate the 80th percentile of profits for each sector
profit_percentile = fortune_df.groupby('sector')['profits'].quantile(0.8).reset_index()
profit_percentile.columns = ['sector', '80th_percentile_profit']

# Find the first occurrence date for each tag
first_occurrence = stackoverflow_df.groupby('tag')['date'].min().reset_index()
first_occurrence.columns = ['tag', 'first_occurrence_date']

# Save the results to CSV files
profit_percentile.to_csv('profit.csv', index=False)
first_occurrence.to_csv('startdates.csv', index=False)
