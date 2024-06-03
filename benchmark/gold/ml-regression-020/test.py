import pandas as pd
from sklearn.model_selection import train_test_split

# 导入CSV文件
data = pd.read_csv('../train.csv')
# 分离标签和特征，假设'diagnosis'是标签列
labels = data[['ID', 'Time_taken(min)']]
features = data.drop(['ID', 'Time_taken(min)'], axis=1)

# 划分数据集，80%为训练集，20%为测试集
features_train, features_test, labels_train, labels_test = train_test_split(
    features, labels, test_size=0.15, random_state=42
)

# 将训练集组合后保存为train.csv
train_df = pd.concat([features_train, labels_train], axis=1)
train_df.to_csv('../train2.csv', index=False)

# 将测试集特征保存为test.csv
features_test.to_csv('../test2.csv', index=False)

# 将测试集标签保存为label.csv
labels_test.to_csv('./submission.csv', index=False)