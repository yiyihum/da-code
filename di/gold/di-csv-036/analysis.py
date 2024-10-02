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
WITH orders_1998 AS (
  SELECT
    o.customerid,
    SUM(od.unitprice * od.quantity) as total
  FROM
    orders o
  INNER JOIN
    order_details od ON o.orderid = od.orderid
  WHERE
    strftime('%Y', o.orderdate) = '1998'
  GROUP BY
    o.customerid
)
SELECT
  c.customerid,
  c.companyname,
  o.total,
  CASE
    WHEN o.total < 1000 THEN 'Low'
    WHEN o.total BETWEEN 1000 AND 5000 THEN 'Medium'
    WHEN o.total BETWEEN 5000 AND 10000 THEN 'High'
    WHEN o.total >= 10000 THEN 'Very High'
  END AS `group`
FROM
  customers c
INNER JOIN
  orders_1998 o ON c.customerid = o.customerid
ORDER BY
  c.customerid;
'''
output_file = "di-csv-036\\gold\\result.csv"
execute_query(query, output_file)