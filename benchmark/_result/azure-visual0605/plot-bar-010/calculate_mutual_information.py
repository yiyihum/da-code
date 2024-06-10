import pandas as pd
import numpy as np
from sklearn.feature_selection import mutual_info_regression
import matplotlib.pyplot as plt

# Load the dataset
data = pd.read_csv('/workspace/data.csv')

# Factorize categorical features
for column in data.select_dtypes(include=['object']).columns:
    data[column], _ = pd.factorize(data[column])

# Identify discrete features
discrete_features = data.select_dtypes(include=['int64']).columns.tolist()

# Calculate mutual information
X = data.drop(columns=['price'])
y = data['price']
mi_scores = mutual_info_regression(X, y, discrete_features=[X.columns.get_loc(c) for c in discrete_features if c in X])

# Create a Series for the mutual information scores
mi_scores = pd.Series(mi_scores, name="MI Scores", index=X.columns)

# Sort the series
mi_scores = mi_scores.sort_values(ascending=False)

# Create a bar chart
plt.figure(figsize=(12, 6))
mi_scores.plot(kind='bar')
plt.title('Mutual Information Score')
plt.xlabel('Variable Names')
plt.ylabel('Mutual Information Score')
plt.tight_layout()

# Save the chart as result.png
plt.savefig('/workspace/result.png')
