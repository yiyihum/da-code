# Compute the mean and standard deviation of the portfolio returns
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import norm

portfolio_losses = pd.read_csv('portfolio.csv')
import pdb; pdb.set_trace()

pm = portfolio_losses.mean()
ps = portfolio_losses.std()

# Compute the 95% VaR using the .ppf()
VaR_95 = norm.ppf(0.95, loc = pm, scale = ps)
# Compute the expected tail loss and the CVaR in the worst 5% of cases
tail_loss = norm.expect(lambda x: x, loc = pm, scale = ps, lb = VaR_95)
CVaR_95 = (1 / (1 - 0.95)) * tail_loss


print("VaR_95:", VaR_95)
print("CVaR_95:", CVaR_95)

# Plot the normal distribution histogram and add lines for the VaR and CVa