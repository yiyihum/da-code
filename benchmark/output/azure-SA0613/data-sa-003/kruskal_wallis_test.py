import pandas as pd
from scipy.stats import kruskal

# Load the dataset
df = pd.read_csv('yulu_bike_sharing_dataset.csv')

# Prepare the data for the Kruskal-Wallis test
groups = df.groupby('weather')['count']

# Perform the Kruskal-Wallis test
stat, p_value = kruskal(*[group for name, group in groups])

# Determine the hypothesis and comment based on the p-value
if p_value > 0.05:
    hypothesis = "No Evidence to Reject Null Hypothesis"
    comment = "No evidence of different distributions"
else:
    hypothesis = "Strong Evidence to Reject Null Hypothesis"
    comment = "Different distributions"

# Prepare the results in the specified format
results = {
    "Test Type": "Non Parametric",
    "Kruskal Statistic": stat,
    "P-Value": p_value,
    "Hypothesis": hypothesis,
    "Comment": comment
}

# Save the results to kruskal_wallis_results.csv
results_df = pd.DataFrame([results])
results_df.to_csv('kruskal_wallis_results.csv', index=False)
