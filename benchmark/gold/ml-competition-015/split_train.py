import pandas as pd
from sklearn.model_selection import train_test_split

data = pd.read_csv('../train.csv')
df = pd.read_csv('../train.csv')
# 删除指定的列
df.drop(['id', 'Hardness'], axis=1, inplace=True)

# 找到全为空的行
missing_rows = df[df.isnull().all(axis=1)]

# 打印全为空的行
print(missing_rows)

data = data.drop_duplicates()
labels = data[['id', 'Hardness']]
features = data.drop('Hardness', axis=1)

features_train, features_test, labels_train, labels_test = train_test_split(
    features, labels, test_size=0.15, random_state=42
)

labels_train = labels_train.drop('id', axis=1)
train_df = pd.concat([features_train, labels_train], axis=1)
train_df.to_csv('../train2.csv', index=False)

features_test.to_csv('../test2.csv', index=False)

labels_test.to_csv('./submission.csv', index=False)
    
