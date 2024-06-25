import pandas as pd

# Load the dataset
df = pd.read_csv('/workspace/ufc-fighters-statistics.csv')

# Filter for undefeated fighters
undefeated_fighters = df[(df['losses'] == 0) & (df['draws'] == 0)]

# Group by weight class and count the number of undefeated fighters
undefeated_count_by_weight_class = undefeated_fighters.groupby('weight_in_kg').size().reset_index(name='undefeated_count')

# Save the result to a CSV file
undefeated_count_by_weight_class.to_csv('/workspace/undefeated.csv', index=False)
