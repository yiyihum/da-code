import pandas as pd

# 假设数据集存储在一个名为'dataset.csv'的文件中
df = pd.read_csv('Kaggle7-1_2\\marketing_data.csv')

# 列出所有的campaign列
campaign_columns = ['AcceptedCmp1', 'AcceptedCmp2', 'AcceptedCmp3', 'AcceptedCmp4', 'AcceptedCmp5']

# 创建一个新的列，其中包含客户接受offer的第一个campaign的编号
def first_accepted_campaign(row):
    for i, col in enumerate(campaign_columns, start=1):
        if row[col] == 1:
            return i
    return None

df['FirstAcceptedCampaign'] = df.apply(first_accepted_campaign, axis=1)

# 计算每一种学历的客户平均在第几次campaign时接受offer
result = df.groupby('Education')['FirstAcceptedCampaign'].mean().reset_index()
result.columns = ['Education', 'AverageCampaignAccepted']

print(result)

result.to_csv('Kaggle7-1_2\\gold\\average_campaign_accepted_by_education.csv', index=False)