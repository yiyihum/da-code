import pandas as pd

# Load the datasets
top_customers = pd.read_csv('Kaggle3-2_2\\gold\\result.csv')
customer_info = pd.read_csv('Kaggle3-2_2\\customers.csv')

# Ensure 'customer_id' is the same type in both DataFrames to avoid merge issues
top_customers['customer_id'] = top_customers['customer_id'].astype(str)
customer_info['customer_id'] = customer_info['customer_id'].astype(str)

# Merge the top customers with the customer info data
merged_data = pd.merge(top_customers, customer_info, on='customer_id', how='left')

# Now, calculate the state counts
state_counts = merged_data['state'].value_counts()

# Get the state with the most top spenders
top_state = state_counts.idxmax()
top_state_count = state_counts.max()

print(f"The state with the most top customers is {top_state} with {top_state_count} customers.")

# Optional: If you want to see the counts for all states, you can print the entire state_counts Series
print(state_counts)