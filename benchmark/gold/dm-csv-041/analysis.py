# Import the pandas library as pd
import pandas as pd

# Read 'police.csv' into a DataFrame named ri
ri = pd.read_csv('DC1-1\\police.csv')

# Drop the 'county_name' and 'state' columns
ri.drop(['county_name', 'state'], axis='columns', inplace=True)

# Drop all rows that are missing 'driver_gender'
ri.dropna(subset=['driver_gender'], inplace=True)

# Change the data type of 'is_arrested' to 'bool'
ri['is_arrested'] = ri.is_arrested.astype('bool')

# Concatenate 'stop_date' and 'stop_time' (separated by a space)
combined = ri.stop_date.str.cat(ri.stop_time, sep=' ')

# Convert 'combined' to datetime format
ri['stop_datetime'] = pd.to_datetime(combined)

# Set 'stop_datetime' as the index
ri.set_index('stop_datetime', inplace=True)

# # Count the unique values in 'violation'
# print(ri.violation.value_counts())

# # Express the counts as proportions
# print(ri.violation.value_counts(normalize=True))

# Create a DataFrame of female drivers
female = ri[ri.driver_gender == 'F']

# Create a DataFrame of male drivers
male = ri[ri.driver_gender == 'M']

# # Compute the violations by female drivers (as proportions)
# print(female.violation.value_counts(normalize=True))

# # Compute the violations by male drivers (as proportions)
# print(male.violation.value_counts(normalize=True))

# Create a DataFrame of female drivers stopped for speeding
female_and_speeding = ri[(ri.driver_gender == 'F') & (ri.violation == 'Speeding')]

# Create a DataFrame of male drivers stopped for speeding
male_and_speeding = ri[(ri.driver_gender == 'M') & (ri.violation == 'Speeding')]

# Compute the stop outcomes for female drivers (as proportions)
print(female_and_speeding.stop_outcome.value_counts(normalize=True))

# Compute the stop outcomes for male drivers (as proportions)
print(male_and_speeding.stop_outcome.value_counts(normalize=True))

import pandas as pd

# Assuming 'ri' DataFrame is already defined
# (The previous code lines related to creating 'female_and_speeding' and 'male_and_speeding' DataFrames are omitted for brevity)

female_outcomes = female_and_speeding.stop_outcome.value_counts(normalize=True)

male_outcomes = male_and_speeding.stop_outcome.value_counts(normalize=True)
outcomes_df = pd.DataFrame({'Female': female_outcomes,
                            'Male': male_outcomes})

outcomes_df.to_csv('stop_outcomes_by_gender.csv')