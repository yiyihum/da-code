import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings("ignore")

# Load the dataset
file_path = '../Books_df.csv'
books_df = pd.read_csv(file_path)

# Remove the 'Unnamed: 0' column
books_df.drop(columns=['Unnamed: 0'], inplace=True)

# Remove currency symbol from 'Price' and convert to float
books_df['Price'] = books_df['Price'].str.replace('₹', '').str.replace(',', '').astype(float)

# Fill missing values in the 'Author' column with "Unknown"
books_df['Author'].fillna('Unknown', inplace=True)

# Price vs. Rating Scatter Plot
plt.figure(figsize=(12, 8), dpi=200)
sns.scatterplot(x='Price', y='Rating', data=books_df, alpha=0.5)
plt.title('Price vs. Rating of Books')
plt.xlabel('Price')
plt.ylabel('Rating')
plt.xscale('log')  # Using a logarithmic scale for better visualization of a wide range of prices
plt.savefig('result.jpg')
plt.show()
