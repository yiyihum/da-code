import warnings
warnings.filterwarnings("ignore")
import numpy as np
import pandas as pd 
import seaborn as sns
from scipy import stats
import sqlite3
from sklearn.datasets import load_breast_cancer
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
#Models
from sklearn.ensemble import RandomForestClassifier

map = {'B': 0, 'M': 1}
id2label = {0: 'B', 1: 'M'}
train_data = pd.read_csv('../train.csv')
test_data = pd.read_csv('../test.csv')
test_data = test_data.drop(["id"], axis=1)
train_data = train_data.drop(["id", "Unnamed: 32"], axis=1)
categorical_col = "diagnosis"

num_cols = list(train_data.select_dtypes('float64').columns)
unrelated_num_cols = []

for i in num_cols:
    # Perform Kruskal-Wallis test
    grouped_data = [train_data[i][train_data[categorical_col] == category] for category in train_data[categorical_col].unique()]
    statistic, p_value = stats.f_oneway(*grouped_data)
    # Set the significance level (alpha)
    alpha = 0.05
    # Print the results with appropriate text color
    if p_value >= alpha:
        unrelated_num_cols.append(i)

train_data = train_data.drop(labels=unrelated_num_cols, axis=1)
test_data = test_data.drop(labels=unrelated_num_cols, axis=1)

input_cols = train_data.columns[:-1]
target_col =  train_data.columns[-1]

inputs_df = train_data[list(input_cols)].copy()
test_df = test_data[list(input_cols)].copy()

targets = [map[label] for label in train_data[(target_col)]]

# Data Scaling
scaler = MinMaxScaler()
scaler.fit(inputs_df[input_cols])
inputs_df[input_cols] = scaler.transform(inputs_df[input_cols])
test_df[input_cols] = scaler.transform(test_df[input_cols])
x_train = inputs_df
y_train = targets

# Handling Class Imbalance
label, counts = np.unique(targets, return_counts=True)
# compute the class weights
counts = max(counts) / counts
class_weights = dict(zip(label, np.around(counts,3)))

model =  RandomForestClassifier(max_depth=5, n_estimators=100, class_weight=class_weights, random_state=42)
model.fit(x_train, y_train)

y_pred = model.predict(test_df)
labels = [id2label[id] for id in y_pred]
labels = pd.DataFrame(labels, columns=['result'])
labels.to_csv('../label.csv', index=False)
