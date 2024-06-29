import pandas as pd

# Load the datasets
assignments = pd.read_csv('/workspace/assignments.csv')
donations = pd.read_csv('/workspace/donations.csv')

# Filter out assignments that have not received any donations
assignments_with_donations = assignments[assignments['assignment_id'].isin(donations['assignment_id'])]

# Join the datasets on assignment_id
merged_data = pd.merge(assignments_with_donations, donations, on='assignment_id')

# Group by assignment_id and region, and calculate the total number of donations for each assignment
grouped_data = merged_data.groupby(['assignment_id', 'assignment_name', 'region', 'impact_score'])['donation_id'].count().reset_index(name='total_donations')

# Select the highest-impact assignment within each region
highest_impact_assignments = grouped_data.loc[grouped_data.groupby('region')['impact_score'].idxmax()]

# Save the resulting data to a CSV file
highest_impact_assignments.to_csv('/workspace/highest_impact_assignments_report.csv', index=False)
