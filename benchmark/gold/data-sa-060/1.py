import pandas as pd
import statsmodels.api as sm

# Read the mortgage delinquency data
mort_del = pd.read_csv('mortgage_delinquency.csv', parse_dates=['Date'])
mort_del.set_index('Date', inplace=True)

# Read the portfolio quarterly minimum returns
port_q_min = pd.read_csv('port_q_min.csv', parse_dates=['Date'])
port_q_min.set_index('Date', inplace=True)
port_q_min = port_q_min.squeeze()  # Convert DataFrame to Series if necessary

# Ensure both series have the same dates
data = pd.concat([mort_del, port_q_min], axis=1).dropna()

# Extract aligned data
mort_del = data['Mortgage Delinquency Rate']
port_q_min = data['port_q_min']

# Add a constant to the regression for the intercept
mort_del = sm.add_constant(mort_del)

# Regress quarterly minimum portfolio returns against mortgage delinquencies
result = sm.OLS(port_q_min, mort_del).fit()

# Retrieve the sum-of-squared residuals
ssr_total = result.ssr
print("Sum-of-squared residuals, 2005-2010: ", ssr_total)
