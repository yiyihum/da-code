import sqlite3
import csv

# 运行'schema.sql'文件来构建数据库
def build_database():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    with open('di-csv-025\Schema.sql', 'r') as f:
        schema = f.read()
        cursor.executescript(schema)
    conn.commit()
    conn.close()

# 执行查询语句，并将结果输出到CSV文件中
def execute_query(query, output_file):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute(query)
    rows = cursor.fetchall()
    with open(output_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(rows)
    conn.close()

# 构建数据库
build_database()

# 执行查询语句，并将结果输出到CSV文件中
query = '''SELECT
  A.CustomerId,
  SUM(A.Balance) AS Total_Balance
FROM accounts AS A
WHERE CustomerID IN (SELECT
  C.CustomerId
FROM customers AS C
INNER JOIN accounts AS A
  ON A.CustomerID = C.CustomerID
WHERE C.City = 'Los Angeles')
GROUP BY A.CustomerId;'''
output_file = "output.csv"
execute_query(query, output_file)