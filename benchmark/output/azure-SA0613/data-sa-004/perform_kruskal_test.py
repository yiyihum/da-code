import pandas as pd
from scipy.stats import kruskal

# Load the dataset
df = pd.read_csv('yulu_bike_sharing_dataset.csv')

# Check if 'weather' and 'count' columns exist and contain more than one unique value for the test to make sense
if 'weather' in df.columns and 'count' in df.columns and df['weather'].nunique() > 1:
    # Prepare the data for the Kruskal-Wallis test
    data_groups = [group["count"].values for name, group in df.groupby('weather')]
    
    # Perform the Kruskal-Wallis test
    kruskal_statistic, p_value = kruskal(*data_groups)
    
    # Determine the hypothesis result
    if p_value > 0.05:
        hypothesis = "No Evidence to Reject Null Hypothesis"
        comment = "No evidence of different distributions"
    else:
        hypothesis = "Strong Evidence to Reject Null Hypothesis"
        comment = "Different distributions"
    
    # Prepare the results
    results = {
        "Test Type": "Non Parametric",
        "Kruskal Statistic": kruskal_statistic,
        "P-Value": p_value,
        "Hypothesis": hypothesis,
        "Comment": comment
    }
    
    # Write the results to weather.csv
    results_df = pd.DataFrame([results])
    results_df.to_csv('weather.csv', index=False)
else:
    print("The 'weather' or 'count' column is missing or does not have enough unique values for the test.")
