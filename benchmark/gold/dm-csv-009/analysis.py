import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the dataset
file_path = 'Kaggle3-1_1\\Books_df.csv'
books_df = pd.read_csv(file_path)

# Remove the 'Unnamed: 0' column
books_df.drop(columns=['Unnamed: 0'], inplace=True)

# Remove currency symbol from 'Price' and convert to float
books_df['Price'] = books_df['Price'].str.replace('₹', '').str.replace(',', '').astype(float)

# Fill missing values in the 'Author' column with "Unknown"
books_df['Author'].fillna('Unknown', inplace=True)

# Set a minimum threshold for the number of ratings to be considered for 'Best Rated Authors'
min_ratings_threshold = 1000

# Group by 'Author' and calculate mean rating, mean price, and total number of ratings
author_stats = books_df.groupby('Author').agg({
    'Rating': 'mean',
    'Price': 'mean',
    'No. of People rated': ['sum', 'mean']
}).reset_index()

# Flatten the multi-level column names
author_stats.columns = ['Author', 'Avg Rating', 'Avg Price', 'Total Ratings', 'Avg Ratings per Book']

# Filter authors to ensure they have a significant number of ratings for reliability
best_rated_authors = author_stats[author_stats['Avg Ratings per Book'] > min_ratings_threshold].sort_values(by='Avg Rating', ascending=False).head(10)

# Identify the most expensive authors
most_expensive_authors = author_stats.sort_values(by='Avg Price', ascending=False).head(10)

# Identify the most rated authors
most_rated_authors = author_stats.sort_values(by='Total Ratings', ascending=False).head(10)

# 打开文件以写入内容
with open('authors_list.txt', 'w', encoding='utf-8') as f:
    # 写入最佳评分作者的名字
    best_rated_authors_names = ', '.join(best_rated_authors['Author'].tolist())
    f.write(f"{best_rated_authors_names}\n")
    
    # 写入最昂贵作者的名字
    most_expensive_authors_names = ', '.join(most_expensive_authors['Author'].tolist())
    f.write(f"{most_expensive_authors_names}\n")
    
    # 写入评分最多的作者的名字
    most_rated_authors_names = ', '.join(most_rated_authors['Author'].tolist())
    f.write(f"{most_rated_authors_names}\n")

# 提示用户文件已保存
print("The authors' names were successfully saved to 'authors_list.txt'.")