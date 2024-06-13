import pandas as pd
import numpy as np
import statsmodels.api as sm
from statsmodels.formula.api import ols

# Load the datasets
mortgage_delinquency = pd.read_csv('mortgage_delinquency.csv', parse_dates=['Date'])
crisis_portfolio = pd.read_csv('crisis_portfolio.csv', parse_dates=['Date'], dayfirst=True)

# Convert the daily portfolio returns to quarterly
crisis_portfolio.set_index('Date', inplace=True)
portfolio_quarterly = crisis_portfolio.resample('QE').last()

# Merge the datasets on the Date column
merged_data = pd.merge(mortgage_delinquency, portfolio_quarterly, left_on='Date', right_index=True)

# Calculate the portfolio returns
merged_data['Portfolio_Return'] = merged_data[['Citibank', 'Morgan Stanley', 'Goldman Sachs', 'J.P. Morgan']].mean(axis=1)

# Define the pre-crisis and post-crisis periods
pre_crisis = merged_data[merged_data['Date'] < '2008-01-01']
post_crisis = merged_data[merged_data['Date'] >= '2008-01-01']

# Perform the Chow test
def chow_test(data_pre, data_post, breakpoint, dependent_var, independent_vars):
    data_full = pd.concat([data_pre, data_post])
    data_full['PostBreak'] = 0
    data_full.loc[breakpoint:, 'PostBreak'] = 1
    for var in independent_vars:
        data_full[f'{var}_PostBreak'] = data_full[var] * data_full['PostBreak']
    
    # Correctly format the variable names within the formula
    independent_vars_formatted = ['Q("{}")'.format(var) for var in independent_vars]
    independent_vars_postbreak = ['Q("{}_PostBreak")'.format(var) for var in independent_vars]
    
    formula_pre = f"{dependent_var} ~ {' + '.join(independent_vars_formatted)}"
    formula_full = f"{dependent_var} ~ {' + '.join(independent_vars_formatted + independent_vars_postbreak)}"
    
    model = ols(formula_pre, data=data_pre).fit()
    model_full = ols(formula_full, data=data_full).fit()
    
    num_params = len(model.params)
    diff_in_ssr = model_full.ssr - model.ssr
    mean_squared_error = model_full.ssr / (data_full.shape[0] - len(model_full.params))
    
    chow_stat = diff_in_ssr / mean_squared_error / num_params
    return chow_stat

# Run the Chow test
chow_statistic = chow_test(pre_crisis, post_crisis, '2008-01-01', 'Portfolio_Return', ['Mortgage Delinquency Rate'])

# Write the result to result.csv
with open('result.csv', 'w') as file:
    file.write('Chow test statistic\n')
    file.write(str(chow_statistic))

print("Chow test statistic calculated and written to result.csv")
