import sqlite3
import csv

# 运行'schema.sql'文件来构建数据库
def build_database():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    with open('di-csv-026\Schema.sql', 'r') as f:
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
query = '''
WITH NO_OF_TRANSACTIONS
AS (SELECT
  T.ACCOUNTID,
  COUNT(TRANSACTIONDATE) AS CNT
FROM transactions T
INNER JOIN accounts A
  ON A.ACCOUNTID = T.ACCOUNTID
GROUP BY T.ACCOUNTID),
BRANCH_INFO
AS (SELECT DISTINCT
  A.BRANCHID,
  B.BRANCHNAME,
  B.CITY
FROM NO_OF_TRANSACTIONS AS C
INNER JOIN accounts AS A
  ON A.ACCOUNTID = C.ACCOUNTID
INNER JOIN BRANCHES AS B
  ON B.BRANCHID = A.BRANCHID
WHERE CNT = (SELECT
  MAX(CNT)
FROM NO_OF_TRANSACTIONS))
SELECT *
FROM BRANCH_INFO;

'''
output_file = "result.csv"
execute_query(query, output_file)