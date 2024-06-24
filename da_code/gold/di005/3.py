import sqlite3
import csv

def execute_query_and_save_to_csv():
    # 连接到 SQLite 数据库
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # SQL 查询语句
    query = """
    SELECT company_original.name, title, rank
    FROM company AS company_original
    LEFT JOIN company AS company_parent ON company_original.parent_id = company_parent.id
    INNER JOIN fortune500 ON COALESCE(company_parent.ticker, company_original.ticker) = fortune500.ticker
    ORDER BY rank;
    """

    try:
        # 执行查询
        cursor.execute(query)
        # 获取所有结果
        results = cursor.fetchall()
        
        # 打印并保存结果到 CSV 文件
        with open('results.csv', 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            # 写入列标题
            writer.writerow([i[0] for i in cursor.description])  # 获取列名并写入作为标题行
            # 写入查询结果
            writer.writerows(results)
            print("Results saved to 'results.csv'")
            
    except sqlite3.Error as e:
        print("An error occurred:", e)
    finally:
        # 关闭游标和连接
        cursor.close()
        conn.close()

if __name__ == '__main__':
    execute_query_and_save_to_csv()
