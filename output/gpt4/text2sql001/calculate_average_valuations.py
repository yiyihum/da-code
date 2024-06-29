import pandas as pd

# Load the merged and filtered data
merged_data = pd.read_csv('/workspace/filtered_merged_data.csv')

# Group by industry and calculate the average valuation
industry_valuations = merged_data.groupby('industry')['valuation'].mean().reset_index()

# Sort the industries by average valuation in descending order
sorted_industries = industry_valuations.sort_values(by='valuation', ascending=False)

# Save the sorted industries with their average valuations to a CSV file
sorted_industries.to_csv('/workspace/sorted_industry_valuations.csv', index=False)

# Output the top industries with the highest average valuations
print(sorted_industries.head())
