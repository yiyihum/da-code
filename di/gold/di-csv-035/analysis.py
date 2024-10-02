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
WITH late_orders AS (
  SELECT
    o.employeeid,
    COUNT(o.employeeid) AS total
  FROM
    orders o
  WHERE
    o.requireddate <= o.shippeddate
  GROUP BY
    o.employeeid
), orders_summary AS (
   SELECT
    o.employeeid,
    COUNT(o.employeeid) AS total
  FROM
    orders o
  GROUP BY
    o.employeeid
)
SELECT
  os.employeeid,
  e.lastname,
  os.total,
  lo.total AS late_orders
FROM
  orders_summary os
INNER JOIN
  employees e ON os.employeeid = e.employeeid
INNER JOIN
  late_orders lo ON os.employeeid = lo.employeeid
ORDER BY
  os.total DESC;
'''
output_file = "di-csv-035\\gold\\result.csv"
execute_query(query, output_file)