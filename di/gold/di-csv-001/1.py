import duckdb
import pandas as pd

# 读取 CSV 文件
data = pd.read_csv('STOCK_PRICE_TIMESERIES.csv')

# 处理日期数据，确保日期格式正确
data['DATE'] = pd.to_datetime(data['DATE']).dt.date

# 创建 DuckDB 连接
con = duckdb.connect(database=':memory:', read_only=False)

# 使用 Pandas DataFrame 创建一个虚拟表
con.register('stock_price_timeseries', data)

# 定义并执行 SQL 查询
sql_query = """
WITH ytd_performance AS (
  SELECT
    ticker,
        MIN(date) OVER (PARTITION BY ticker) AS start_of_year_date,
        FIRST_VALUE(value) OVER (PARTITION BY ticker ORDER BY date ASC ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS start_of_year_price,
        MAX(date) OVER (PARTITION BY ticker) AS latest_date,
        LAST_VALUE(value) OVER (PARTITION BY ticker ORDER BY date ASC ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) AS latest_price
  FROM stock_price_timeseries
  WHERE
    ticker IN ('AAPL', 'MSFT', 'AMZN', 'GOOGL', 'META', 'TSLA', 'NVDA')
    AND date >= DATE_TRUNC('YEAR', CURRENT_DATE()) 
    AND variable_name = 'Post-Market Close'
)
SELECT
  ticker,
  start_of_year_date,
  start_of_year_price,
  latest_date,
  latest_price,
  (latest_price - start_of_year_price) / start_of_year_price * 100 AS percentage_change_ytd
FROM
  ytd_performance
GROUP BY
  ticker, start_of_year_date, start_of_year_price, latest_date, latest_price
ORDER BY percentage_change_ytd DESC;
"""

# 执行查询并获取结果
result = con.execute(sql_query).fetchdf()
result.to_csv('result.csv', index=False)

# 打印结果
print(result)

# 关闭连接
con.close()
