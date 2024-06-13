import pandas as pd
import statsmodels.api as sm

# Load the dataset
df = pd.read_csv('FamaFrenchFactors.csv')

# Define the independent variables (factors) and the dependent variable
X = df[['Market_Excess', 'SMB', 'HML']]  # Independent variables
y = df['Portfolio']  # Dependent variable

# Add a constant to the model (intercept)
X = sm.add_constant(X)

# Fit the regression model
model = sm.OLS(y, X).fit()

# Get the adjusted R-squared value
adjusted_r_squared = model.rsquared_adj
print(f"Adjusted R-squared: {adjusted_r_squared}")

# Save the regression results to a CSV file in the specified format
results_df = pd.DataFrame({
    'Intercept': [model.params[0]],
    'Market_Excess': [model.params[1]],
    'SMB': [model.params[2]],
    'HML': [model.params[3]],
    'Adjusted_R_squared': [adjusted_r_squared]
})
results_df.to_csv('result.csv', index=False)
