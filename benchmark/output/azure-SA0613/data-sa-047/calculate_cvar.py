import pandas as pd
import numpy as np
from scipy.stats import t, gaussian_kde
from scipy.integrate import quad

# Load the dataset
data = pd.read_csv('GE - Historical.csv')

# Calculate daily returns as percentage change in the Adjusted Close price
data['returns'] = data['Adj Close'].pct_change()

# Drop any rows with NaN values in the 'returns' column
data = data.dropna(subset=['returns'])

# Fit a T distribution to the data
params = t.fit(data['returns'])

# Estimate the 99% VaR for the T distribution
t_var_99 = t.ppf(0.01, *params)

# Calculate the 99% CVaR for the T distribution
# CVaR should be negative, representing a loss
t_cvar_99 = -t.expect(lambda x: -x if x <= t_var_99 else 0, args=(params[0],), loc=params[1], scale=params[2])

# Fit a Gaussian KDE to the data
kde = gaussian_kde(data['returns'])

# Estimate the 99% VaR for the KDE
kde_support = np.linspace(data['returns'].min(), data['returns'].max(), 1000)
kde_cdf = np.array([kde.integrate_box_1d(-np.inf, x) for x in kde_support])
kde_var_99_index = np.searchsorted(kde_cdf, 0.01)
kde_var_99 = kde_support[kde_var_99_index]

# Calculate the 99% CVaR for the KDE
# CVaR should be negative, representing a loss
# The integration should be from -infinity to the VaR (not the other way around)
# The error in the previous code was not negating the result of the integration
# This time we ensure the result is negated
kde_cvar_99, _ = quad(lambda x: x * kde(x), -np.inf, kde_var_99)
kde_cvar_99 = -kde_cvar_99  # Negate the result to ensure the CVaR is negative

# Save the corrected results to the result.csv file
results = pd.DataFrame({
    'Distribution': ['T', 'KDE'],
    'VaR_99': [t_var_99, kde_var_99],
    'CVaR_99': [t_cvar_99, kde_cvar_99]
})
results.to_csv('result.csv', index=False)
