import pandas as pd
from sklearn.model_selection import train_test_split

data = pd.read_csv('../train.csv')

# 分离标签和特征，假设'diagnosis'是标签列
labels = data[['Id', 'SalePrice']]
features = data.drop('SalePrice', axis=1)

features_train, features_test, labels_train, labels_test = train_test_split(
    features, labels, test_size=0.15, random_state=42
)

labels_train = labels_train.drop('Id', axis=1)
train_df = pd.concat([features_train, labels_train], axis=1)
train_df.to_csv('../train.csv', index=False)

features_test.to_csv('../test.csv', index=False)

labels_test.to_csv('./submission.csv', index=False)
    
