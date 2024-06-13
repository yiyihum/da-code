import pandas as pd
from scipy.stats import shapiro

# Load the dataset
df = pd.read_csv('yulu_bike_sharing_dataset.csv')

# Group the data into holidays (grpA) and working days (grpB)
grpA = df[df['holiday'] == 1]['count']
grpB = df[df['workingday'] == 1]['count']

# Perform Shapiro-Wilk normality test on both groups
ntA_stat, ntA_p = shapiro(grpA)
ntB_stat, ntB_p = shapiro(grpB)

# Output the results of the normality test
normality_results = {
    'Group': ['A', 'B'],
    'Statistic': [ntA_stat, ntB_stat],
    'p-value': [ntA_p, ntB_p]
}

normality_df = pd.DataFrame(normality_results)
print(normality_df)
