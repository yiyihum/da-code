import pandas as pd

# Load the undefeated fighters count by weight
undefeated_df = pd.read_csv('/workspace/undefeated.csv')

# Define the weight class boundaries and names
weight_classes = [
    (0, 57.0, 'Flyweight'),
    (57.1, 61.2, 'Bantamweight'),
    (61.3, 65.8, 'Featherweight'),
    (65.9, 70.0, 'Lightweight'),
    (70.1, 77.1, 'Welterweight'),
    (77.2, 83.9, 'Middleweight'),
    (84.0, 93.0, 'Light Heavyweight'),
    (93.1, float('inf'), 'Heavyweight')
]

# Function to determine the weight class based on weight
def get_weight_class(weight):
    for lower_bound, upper_bound, weight_class in weight_classes:
        if lower_bound <= weight <= upper_bound:
            return weight_class
    return 'Unknown Weight Class'

# Map the weight in kg to weight class names
undefeated_df['weight_class'] = undefeated_df['weight_in_kg'].apply(get_weight_class)

# Drop the weight_in_kg column as it's no longer needed
undefeated_df.drop('weight_in_kg', axis=1, inplace=True)

# Reorder columns to have weight class first
undefeated_df = undefeated_df[['weight_class', 'undefeated_count']]

# Save the updated dataframe to the CSV file
undefeated_df.to_csv('/workspace/undefeated.csv', index=False)
