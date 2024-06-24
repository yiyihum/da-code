import pandas as pd
from sqlalchemy import create_engine

# 创建数据库引擎，这里数据库名为database.db
engine = create_engine('sqlite:///database.db')

# 读取CSV文件
df = pd.read_csv('Salaries.csv')

# 处理数据，将空白字符串转换为None，以兼容数据库中的NULL
df = df.replace({'': None})

# 使用pandas的to_sql函数将DataFrame导入到SQLite数据库中的employees表
df.to_sql('employees', con=engine, index=False, if_exists='append')

print("Data has been successfully loaded into the database.")
