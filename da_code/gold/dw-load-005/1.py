from sqlalchemy import create_engine, Column, Integer, String, Float, MetaData, Table

# 创建数据库引擎，这里数据库名为database.db
engine = create_engine('sqlite:///database.db')

# 初始化元数据
metadata = MetaData()

# 定义表结构
employees = Table('employees', metadata,
                  Column('Id', Integer, primary_key=True),
                  Column('EmployeeName', String),
                  Column('JobTitle', String),
                  Column('BasePay', Float),
                  Column('OvertimePay', Float),
                  Column('OtherPay', Float),
                  Column('Benefits', Float, nullable=True),  # 允许为空
                  Column('TotalPay', Float),
                  Column('TotalPayBenefits', Float),
                  Column('Year', Integer),
                  Column('Notes', String, nullable=True),  # 允许为空
                  Column('Agency', String),
                  Column('Status', String, nullable=True)  # 允许为空
                 )

# 创建表
metadata.create_all(engine)

print("Database and table have been created.")
