import sqlite3
import csv

# 运行'schema.sql'文件来构建数据库
def build_database():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    with open('di-csv-031\\northwind.sql', 'r', encoding='utf-8') as f:
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
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerows(rows)
    conn.close()

# 构建数据库
# build_database()

# 执行查询语句，并将结果输出到CSV文件中
query = '''
SELECT
  c.customerid,
  c.companyname,
  ROUND(SUM(od.unitprice * od.quantity), 2) AS total_amount
FROM
  customers c
INNER JOIN
  orders o ON c.customerid = o.customerid
INNER JOIN
  order_details od ON o.orderid = od.orderid
WHERE
  strftime('%Y', o.orderdate) = '1998'
GROUP BY
  c.customerid, c.companyname
HAVING
  SUM(od.unitprice * od.quantity) >= 15000
ORDER BY
  total_amount DESC;
'''
output_file = "result.csv"
execute_query(query, output_file)