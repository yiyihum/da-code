
import sqlite3  # For connecting to SQLite database
import pandas as pd  # For data manipulation and analysis
import numpy as np  # For numerical operations
from sklearn.model_selection import train_test_split  # For splitting data into training and testing sets
from sklearn.ensemble import RandomForestClassifier  # For building a Random Forest classifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix  # For evaluating model performance
import matplotlib.pyplot as plt  # For data visualization
import seaborn as sns  # For enhanced data visualization

# Additional libraries for data manipulation and visualization
import datetime  # For working with date and time data
from sklearn.preprocessing import StandardScaler  # For feature scaling
from sklearn.metrics import roc_auc_score, roc_curve  # For ROC curve analysis
from sklearn.model_selection import cross_val_score, GridSearchCV  # For hyperparameter tuning
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.linear_model import LinearRegression

db_path = './olist.sqlite'
db_connection = sqlite3.connect(db_path)


def execute_query(query):
    return pd.read_sql_query(query, db_connection)

# Explore tables in the database
tables_query = "SELECT name FROM sqlite_master WHERE type='table';"
tables = execute_query(tables_query)

# Display tables in a structured format
print("Tables in the database:")
print(tables)


# Distribution of product categories
product_category_query = "SELECT product_category_name, COUNT(*) AS count FROM products GROUP BY product_category_name ORDER BY count DESC LIMIT 10;"
product_category_data = execute_query(product_category_query)

plt.figure(figsize=(12, 8))
sns.barplot(x='product_category_name', y='count', data=product_category_data)
plt.title('Top 10 Product Categories by Count')
plt.xlabel('Product Category')
plt.ylabel('Count')
plt.xticks(rotation=30)
plt.savefig('result.png')
plt.show()