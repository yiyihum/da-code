import pandas as pd

df = pd.read_csv('../parking_violation.csv')

# 添加一个标记列用于标记重复行
df['duplicate'] = df.duplicated(subset=['Plate ID', 'Issue Date', 'Violation Time', 'House Number', 'Street Name'], keep='first')

# 删除标记为重复的行
df_cleaned = df[~df['duplicate']]

# 删除辅助的标记列
df_cleaned = df_cleaned.drop(columns=['duplicate'])

# 将清理后的DataFrame写回CSV文件或数据库
df_cleaned.to_csv('cleaned_parking_violation.csv', index=False)

print("重复行已删除并保存为cleaned_parking_violation.csv")
