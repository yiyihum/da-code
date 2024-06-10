import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the dataset
file_path = '../Books_df.csv'
books_df = pd.read_csv(file_path)

# Remove the 'Unnamed: 0' column
books_df.drop(columns=['Unnamed: 0'], inplace=True)

# Remove currency symbol from 'Price' and convert to float
books_df['Price'] = books_df['Price'].str.replace('₹', '').str.replace(',', '').astype(float)

# Check for missing values
missing_values = books_df.isnull().sum()

# Check datatypes of all columns after initial cleanup
dtypes_after_cleanup = books_df.dtypes

# Fill missing values in the 'Author' column with "Unknown"
books_df['Author'].fillna('Unknown', inplace=True)

# Group by 'Author' and calculate mean price
author_stats = books_df.groupby('Author')['Price'].mean().reset_index()

# Sort authors by average price in descending order and get the top author
most_expensive_author = author_stats.sort_values(by='Price', ascending=False).head(10)

plt.figure(figsize=(18, 12))
sns.barplot(y='Author', x='Price', data=most_expensive_author, palette='autumn', orient='h')
plt.title('Most Expensive Author')
plt.xlabel('Average Price')
plt.ylabel('Author')
plt.savefig('./result.jpg')