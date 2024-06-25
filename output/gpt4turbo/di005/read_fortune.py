import pandas as pd

# Load the Fortune 500 data
fortune_data = pd.read_csv('/workspace/fortune.csv')

# Since the data is already ranked, we just need to display it
# However, we will sort it by rank to ensure it is in the correct order
fortune_sorted = fortune_data.sort_values(by='rank')

# Save the sorted data to a new CSV file
fortune_sorted.to_csv('/workspace/fortune_ranked.csv', index=False)
print("Ranked Fortune 500 list saved to fortune_ranked.csv")
