import pandas as pd

# Load the dataset
df = pd.read_csv('Books_df.csv')

# Clean the Price column and convert it to float
df['Price'] = df['Price'].replace('[₹,]', '', regex=True).astype(float)

# Group by Author and calculate mean rating and sum of ratings
author_rating = df.groupby('Author')['Rating'].mean().nlargest(10)
author_rating_count = df.groupby('Author')['No. of People rated'].sum().nlargest(10)

# Group by Author and find the max price
author_price = df.groupby('Author')['Price'].max().nlargest(10)

# Create a new DataFrame to store the results
results = pd.DataFrame({
    'Best-Rated Author': author_rating.index,
    'Most Expensive Author': author_price.index,
    'Most Rated Author': author_rating_count.index
})

# Save the results to 'author.csv'
results.to_csv('author.csv', index=False)
