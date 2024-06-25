import pandas as pd

# Load the updated undefeated fighters count by weight class
undefeated_df = pd.read_csv('/workspace/undefeated.csv')

# Aggregate the counts by weight class, excluding 'Unknown Weight Class'
aggregated_df = undefeated_df[undefeated_df['weight_class'] != 'Unknown Weight Class']     .groupby('weight_class', as_index=False).sum()

# Save the aggregated counts to the CSV file
aggregated_df.to_csv('/workspace/undefeated.csv', index=False)
