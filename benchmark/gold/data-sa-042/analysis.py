import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the dataset
file_path = 'Kaggle3-1_0\\Books_df.csv'
books_df = pd.read_csv(file_path)

# Remove the 'Unnamed: 0' column
books_df.drop(columns=['Unnamed: 0'], inplace=True)

# Remove currency symbol from 'Price' and convert to float
books_df['Price'] = books_df['Price'].str.replace('₹', '').str.replace(',', '').astype(float)

# Fill missing values in the 'Author' column with "Unknown"
books_df['Author'].fillna('Unknown', inplace=True)

# Define a function to detect outliers based on the IQR method
def detect_outliers_iqr(data, feature):
    Q1 = data[feature].quantile(0.25)
    Q3 = data[feature].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    
    outliers = data[(data[feature] < lower_bound) | (data[feature] > upper_bound)]
    return outliers, lower_bound, upper_bound

# Detect outliers for 'Price'
price_outliers, price_lb, price_ub = detect_outliers_iqr(books_df, 'Price')

# Detect outliers for 'No. of People rated'
rating_outliers, rating_lb, rating_ub = detect_outliers_iqr(books_df, 'No. of People rated')

# Summary of outliers detected
outliers_summary = {
    'Price': {
        'Number of Outliers': price_outliers.shape[0],
        'Lower Bound': price_lb,
        'Upper Bound': price_ub
    },
    'No. of People rated': {
        'Number of Outliers': rating_outliers.shape[0],
        'Lower Bound': rating_lb,
        'Upper Bound': rating_ub
    }
}

import json

# 指定要保存的json文件路径
json_file_path = 'Kaggle3-1_0\\gold\\result.json'

# 将汇总字典转换为json字符串，然后保存到文件
with open(json_file_path, 'w') as json_file:
    json.dump(outliers_summary, json_file, indent=4)