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
WITH TOTAL_BALANCE
AS (SELECT
  BRANCHID,
  SUM(BALANCE) AS SUM_BAL
FROM ACCOUNTS
GROUP BY BRANCHID)
SELECT
  B.*,
  A.SUM_BAL
FROM TOTAL_BALANCE AS A
LEFT JOIN BRANCHES AS B
  ON A.BRANCHID = B.BRANCHID
WHERE A.SUM_BAL = (SELECT
  MAX(SUM_BAL)
FROM TOTAL_BALANCE);


'''
output_file = "result.csv"
execute_query(query, output_file)