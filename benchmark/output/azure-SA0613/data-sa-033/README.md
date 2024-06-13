# GEV risk estimation

Suppose that you were holding € 1,000,000 of GE stock on January 1, 2010. You would like to cover the** ***expected* maximum losses that might occur over the next week, based upon available data from the previous two years, 2008 - 2009. You assume that maximum weekly losses for GE are distributed according to a Generalized Extreme Value (GEV) distribution.** **

To model expected losses you'll estimate the CVaR at the 99% confidence level for the GEV distribution, and use it to compute the amount needed in reserve to cover the expected maximum weekly loss over January, 2010.

The** **`genextreme` distribution from** **`scipy.stats` is available in your workspace, as is GE's** **`losses` for the 2008 - 2009 period.
