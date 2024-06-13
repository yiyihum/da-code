import pandas as pd
import numpy as np

# Load the dataset
data = pd.read_csv('monthly_deaths.csv', parse_dates=['date'])

# Split the data into before and after handwashing was introduced
handwashing_start = pd.to_datetime('1847-01-01')
before_handwashing = data[data['date'] < handwashing_start]
after_handwashing = data[data['date'] >= handwashing_start]

# Calculate the death rate before and after handwashing
death_rate_before = before_handwashing['deaths'] / before_handwashing['births']
death_rate_after = after_handwashing['deaths'] / after_handwashing['births']

# Perform bootstrap analysis
bootstrap_samples = 10000
mean_diffs = []

for _ in range(bootstrap_samples):
    before_sample = death_rate_before.sample(n=len(death_rate_before), replace=True)
    after_sample = death_rate_after.sample(n=len(death_rate_after), replace=True)
    mean_diff = before_sample.mean() - after_sample.mean()
    mean_diffs.append(mean_diff)

# Calculate the 95% confidence interval
confidence_interval = np.percentile(mean_diffs, [2.5, 97.5])

# Write the results to the result.csv file
results = pd.DataFrame({
    'Bootstrap Mean Reduction': [np.mean(mean_diffs)],
    '95% CI Lower': [confidence_interval[0]],
    '95% CI Upper': [confidence_interval[1]]
})
results.to_csv('result.csv', index=False)
