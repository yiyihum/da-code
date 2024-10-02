import sqlite3
import csv

def insert_data_from_csv(conn, csv_file, table_name):
    cursor = conn.cursor()
    with open(csv_file, newline='', encoding='utf-8') as file:
        dr = csv.DictReader(file)
        if table_name == "company":
            to_db = [(i['id'], i['exchange'], i['ticker'], i['name'], i.get('parent_id')) for i in dr]
        elif table_name == "tag_company":
            to_db = [(i['tag'], i['company_id']) for i in dr]
        elif table_name == "fortune500":
            to_db = [(i['rank'], i['title'], i['name'], i['ticker'], i['url'], i['hq'], i['sector'],
                      i['industry'], i['employees'], i['revenues'], i['revenues_change'],
                      i['profits'], i['profits_change'], i['assets'], i['equity']) for i in dr]

        columns = ', '.join(dr.fieldnames)
        placeholders = ', '.join(['?' for _ in dr.fieldnames])
        sql = f'INSERT INTO {table_name} ({columns}) VALUES ({placeholders})'
        cursor.executemany(sql, to_db)
    
    conn.commit()
    cursor.close()

def main():
    database = 'database.db'
    conn = sqlite3.connect(database)
    try:
        # 插入数据到 company 表
        insert_data_from_csv(conn, 'company.csv', 'company')
        # 插入数据到 fortune500 表
        insert_data_from_csv(conn, 'fortune.csv', 'fortune500')
        print("Data inserted successfully.")
    except Exception as e:
        print("An error occurred:", e)
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    main()
