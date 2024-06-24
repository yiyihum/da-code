import pandas as pd
import statsmodels.api as sm

# Read the data
mort_del = pd.read_csv("mortgage_delinquency.csv", parse_dates=['Date'], index_col='Date')
port_q_min = pd.read_csv("port_q_min.csv", parse_dates=['Date'], index_col='Date')

# Merge the data on Date
data = pd.merge(mort_del, port_q_min, left_index=True, right_index=True)

# Rename columns for clarity
data.columns = ['mort_del', 'returns']

# Split the data into before and after June 30, 2008
before = data.loc[:'2008-06-30']
after = data.loc['2008-07-01':]

# Add intercept constants to each sub-period 'before' and 'after'
before_with_intercept = sm.add_constant(before['mort_del'])
after_with_intercept = sm.add_constant(after['mort_del'])

# Fit OLS regressions to each sub-period
r_b = sm.OLS(before['returns'], before_with_intercept).fit()
r_a = sm.OLS(after['returns'], after_with_intercept).fit()

# Get sum-of-squared residuals for both regressions
ssr_before = r_b.ssr
ssr_after = r_a.ssr

# Get the total sum-of-squared residuals for the combined period
combined_with_intercept = sm.add_constant(data['mort_del'])
combined_model = sm.OLS(data['returns'], combined_with_intercept).fit()
ssr_total = combined_model.ssr

# Compute and display the Chow test statistic
numerator = ((ssr_total - (ssr_before + ssr_after)) / 2)
denominator = ((ssr_before + ssr_after) / (len(data) - 4))
chow_test_statistic = numerator / denominator

print("Chow test statistic: ", chow_test_statistic)

