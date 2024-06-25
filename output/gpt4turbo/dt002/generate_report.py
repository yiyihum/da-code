import pandas as pd

# Load the datasets
donations_df = pd.read_csv('donations.csv')
assignments_df = pd.read_csv('assignments.csv')
donors_df = pd.read_csv('donors.csv')

# Join the donations data with the donors data to get the donor types
donations_with_donor_type = donations_df.merge(donors_df[['donor_id', 'donor_type']], on='donor_id', how='left')

# Aggregate the total donation amounts by assignment_id and donor type
total_donations = donations_with_donor_type.groupby(['assignment_id', 'donor_type'])['amount'].sum().reset_index()

# Join the aggregated donation data with the assignments data
joined_df = total_donations.merge(assignments_df[['assignment_id', 'assignment_name', 'region']], on='assignment_id', how='left')

# Select the required columns and sort by the total donation amount in descending order
top_assignments = joined_df[['assignment_name', 'region', 'donor_type', 'amount']].copy()
top_assignments.rename(columns={'amount': 'total_donation_amount'}, inplace=True)
top_assignments['total_donation_amount'] = top_assignments['total_donation_amount'].round()  # Round the amounts
top_assignments = top_assignments.sort_values(by='total_donation_amount', ascending=False).head(5)

# Save the top five assignments to a CSV file
top_assignments.to_csv('/workspace/top_five_assignments.csv', index=False)
