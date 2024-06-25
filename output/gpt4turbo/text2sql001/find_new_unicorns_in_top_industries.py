import pandas as pd

# Load the merged and filtered data
merged_data = pd.read_csv('/workspace/filtered_merged_data.csv')

# Top industries with the highest average valuations
top_industries = [
    "Consumer & retail",
    "Auto & transportation",
    "Data management & analytics",
    "Fintech",
    "Travel"
]

# Filter for new unicorns in the top industries
new_unicorns_in_top_industries = merged_data[merged_data['industry'].isin(top_industries)]

# Save the new unicorns in top industries to a CSV file
new_unicorns_in_top_industries.to_csv('/workspace/new_unicorns_in_top_industries.csv', index=False)

# Output the new unicorns in top industries
print(new_unicorns_in_top_industries[['company', 'industry', 'valuation', 'date_joined']])
