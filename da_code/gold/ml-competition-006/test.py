import pandas as pd
from sklearn.model_selection import train_test_split

data = pd.read_csv('../train.csv')

labels = data[['Id', 'quality']]
features = data.drop('quality', axis=1)

features_train, features_test, labels_train, labels_test = train_test_split(
    features, labels, test_size=0.15, random_state=42, stratify=data['quality']
)

labels_train.drop('Id', axis=1, inplace=True)
train_df = pd.concat([features_train, labels_train], axis=1)
train_df.to_csv('../train2.csv', index=False)


features_test.to_csv('../test.csv', index=False)

labels_test.to_csv('./submission.csv', index=False)
