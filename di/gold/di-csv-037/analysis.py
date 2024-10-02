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
WITH countries AS (
  SELECT
    country
  FROM
    suppliers
  UNION
  SELECT
    country
  FROM
    customers
), suppliercountry AS (
  SELECT
    DISTINCT country
  FROM
    suppliers
), customercountry AS (
  SELECT
    DISTINCT country
  FROM
    customers
)
SELECT
  sp.country AS supplier_country,
  cp.country AS customer_country
FROM
  countries c
LEFT JOIN
  suppliercountry sp ON c.country = sp.country
LEFT JOIN
  customercountry cp ON c.country = cp.country;
'''
output_file = "di-csv-037\\gold\\result.csv"
execute_query(query, output_file)