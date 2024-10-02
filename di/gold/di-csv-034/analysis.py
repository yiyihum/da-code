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
WITH repeated_quantities AS (
    SELECT
      od.orderid
    FROM
      order_details od
      INNER JOIN
      orders o ON od.orderid = o.orderid
    WHERE
      od.quantity >= 60
    GROUP BY
      od.orderid, od.quantity
    HAVING
      COUNT(od.quantity) > 1
    ORDER BY
      od.orderid
)
SELECT
  od.orderid,
  od.productid,
  od.unitprice,
  od.quantity,
  od.discount
FROM
  order_details od
WHERE
  od.orderid IN (SELECT orderid FROM repeated_quantities);
'''
output_file = "di-csv-034\\result.csv"
execute_query(query, output_file)