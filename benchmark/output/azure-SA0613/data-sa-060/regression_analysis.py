import pandas as pd
from sklearn.linear_model import LinearRegression
import numpy as np

# Load the datasets
portfolio_data = pd.read_csv('port_q_min.csv')
delinquency_data = pd.read_csv('mortgage_delinquency.csv')

# Merge the datasets on the Date column
merged_data = pd.merge(portfolio_data, delinquency_data, on='Date')

# Perform linear regression
X = merged_data[['Mortgage Delinquency Rate']].values
y = merged_data['port_q_min'].values
model = LinearRegression()
model.fit(X, y)

# Calculate the sum of squared residuals (SSR)
predictions = model.predict(X)
residuals = y - predictions
SSR = np.sum(residuals**2)

# Save the SSR result to a CSV file in the format of sample_result.csv
result_df = pd.DataFrame({'SSR': [SSR]})
result_df.to_csv('result.csv', index=False)
