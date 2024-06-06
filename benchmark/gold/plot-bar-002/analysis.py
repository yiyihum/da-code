import numpy as np  # Linear algebra library for Python.
import pandas as pd  # Data processing library, particularly useful for handling CSV files.
import matplotlib.pyplot as plt  # Library for creating static, animated, and interactive visualizations in Python.
import seaborn as sns  # Statistical data visualization library based on matplotlib.
import sqlite3  # Library to interact with SQLite database.

# Connect to the Zomato SQLite database.
con = sqlite3.connect('../zomato_rawdata.sqlite')
# Read the 'Users' table into a DataFrame.
df = pd.read_sql_query("SELECT * FROM Users", con)

# Display the number of missing values in each column.
number_of_missing_values = df.isnull().sum()
# Calculate the percentage of missing values for each column.
percentage_of_missing_values = df.isnull().sum() / len(df) * 100
# List all unique values in the 'rate' column.
unique_rate_values = df['rate'].unique()
# Replace 'NEW' and '-' with NaN (Not a Number) in the 'rate' column.
df['rate'].replace(('NEW', '-'), np.nan, inplace=True)
# Verify that the values were replaced by checking the unique values in 'rate' again.
unique_rate_values_post_replacement = df['rate'].unique()

# Convert the 'rate' column to a float, ignoring any entries that are not strings.
df['rate'] = df['rate'].apply(lambda x: float(x.split('/')[0]) if isinstance(x, str) else x)

# Create a crosstab of ratings against online order presence.
x = pd.crosstab(df['rate'], df['online_order'])

# Normalize the crosstab by dividing by the sum along rows and multiply by 100 to get percentages.
normalize_df = x.div(x.sum(axis=1).astype(float), axis=0)
# Plot the normalized crosstab as a stacked bar chart.
(normalize_df * 100).plot(kind='bar', stacked=True)

# Show the plot.
plt.title('Percentage of Restaurants\' Online Order Option by Rating')
plt.xlabel('Rating')
plt.ylabel('Percentage of Online Orders')

# Save the figure to a JPG file named 'online_order_percentage_by_rating.jpg'.
plt.savefig('./result.jpg')

# Show the plot.
plt.show()