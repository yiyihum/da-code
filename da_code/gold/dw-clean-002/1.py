import pandas as pd
import sqlite3
import re

# 连接到SQLite数据库
conn = sqlite3.connect('../parking_violation.db')

# 读取数据到DataFrame中
df = pd.read_sql_query("SELECT * FROM parking_violation", conn)

# 更新violation_location，使其左填充为4位数
df['Violation Location'] = df['Violation Location'].astype(str).str.zfill(4)

# 更新vehicle_body_type，替换'P-U'为'TRK'
df['Vehicle Body Type'] = df['Vehicle Body Type'].str.replace('P-U', 'TRK')

# 更新street_name，使其首字母大写
df['Street Name'] = df['Street Name'].str.title()

# 更新plate_id，将其中的字母替换为'-'
df['Plate ID'] = df['Plate ID'].apply(lambda x: re.sub(r'[A-Z]', '-', x))

# 将DataFrame写回SQLite数据库
df.to_sql('parking_violation', conn, if_exists='replace', index=False)

# 关闭数据库连接
conn.close()

print("数据库处理完成")
