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



# Query to get the count of orders for each order status over time
order_status_time_query = """
SELECT strftime('%Y-%m', order_purchase_timestamp) AS month, 
       order_status, 
       COUNT(*) AS count
FROM orders
GROUP BY strftime('%Y-%m', order_purchase_timestamp), order_status
ORDER BY month;
"""

# Execute query and fetch data
order_status_time_data = execute_query(order_status_time_query)

# Plotting the trend of order statuses over time
plt.figure(figsize=(18, 6))
sns.lineplot(x='month', y='count', hue='order_status', data=order_status_time_data)
plt.title('Trend of Order Statuses Over Time')
plt.xlabel('Month')
plt.grid(False)
plt.ylabel('Order Count')
plt.xticks(rotation=45)
plt.legend(title='Order Status')
plt.savefig('result.png')
plt.show()
