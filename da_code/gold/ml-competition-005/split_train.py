import pandas as pd
from sklearn.model_selection import train_test_split

# 导入CSV文件
data = pd.read_csv('../train.csv')

# 分离标签和特征，假设'diagnosis'是标签列
labels = data[['id', 'Status']]
features = data.drop('Status', axis=1)

# 划分数据集，80%为训练集，20%为测试集
features_train, features_test, labels_train, labels_test = train_test_split(
    features, labels, test_size=0.15, random_state=42, stratify=data['Status']
)

# 将训练集组合后保存为train.csv
labels_train.drop('id', axis=1, inplace=True)
train_df = pd.concat([features_train, labels_train], axis=1)
train_df.to_csv('../train2.csv', index=False)

# 将测试集特征保存为test.csv
features_test.to_csv('../test.csv', index=False)

Status_D = []
Status_C = []
Status_CL = []

labels = labels_test['Status']

for label in labels:
    if label =='C':
        Status_C.append(1)
        Status_D.append(0)
        Status_CL.append(0)
    elif label == 'D':
        Status_C.append(0)
        Status_D.append(1)
        Status_CL.append(0)
    elif label == 'CL':
        Status_C.append(0)
        Status_D.append(0)
        Status_CL.append(1)

labels_test['Status_C'] = Status_C
labels_test['Status_CL'] = Status_CL
labels_test['Status_D'] = Status_D

labels_test.drop('Status', axis=1, inplace=True)

labels_test.to_csv('./submission.csv', index=False)
    
