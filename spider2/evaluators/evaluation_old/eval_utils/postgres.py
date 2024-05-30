import psycopg2
import xml.etree.ElementTree as ET

def get_postgres_schema(url):
    conn = psycopg2.connect(url)
    cur = conn.cursor()

    # Fetch table names and column details
    cur.execute("""
        SELECT schema_name
        FROM information_schema.schemata;
    """)
    schema_data = cur.fetchall()

    cur.close()
    conn.close()
    
    schemas = [item[0] for item in schema_data if item[0] != 'information_schema' and item[0] != 'pg_catalog']
    if len(schemas) > 1:
        schemas.remove('public')
        return schemas[0]
    else:
        return 'public'


def get_postgres_tables(url, schema="public"):
    conn = psycopg2.connect(url)
    cur = conn.cursor()

    # Fetch table names and column details
    cur.execute(f"""
    SELECT table_name
    FROM information_schema.tables
    WHERE table_schema = '{schema}';
    """)
    table_data = cur.fetchall()

    cur.close()
    conn.close()

    return [item[0] for item in table_data]  

def get_postgres_columns(url, table, schema='public'):
    conn = psycopg2.connect(url)
    cur = conn.cursor()

    # Fetch table names and column details
    cur.execute(f"""
    SELECT column_name
    FROM information_schema.columns
    WHERE table_schema = '{schema}' and table_name = '{table}';
    """)
    schema_data = cur.fetchall()

    cur.close()
    conn.close()
    
    return [item[0] for item in schema_data]  

def execute_query(url, sql_query):
    try:
        conn = psycopg2.connect(url)
        cursor = conn.cursor()
        cursor.execute(sql_query)

        result = cursor.fetchall()

        conn.commit()
        cursor.close()
        conn.close()

        return result

    except psycopg2.Error as e:
        print(f"Error: {e}")
        return None
    
import csv
def execute_query_to_csv(url, query, csv_file_path):
    connection = psycopg2.connect(url)
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        import pdb; pdb.set_trace()
        with open(csv_file_path, 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow([desc[0] for desc in cursor.description])
            csv_writer.writerows(result)
    finally:
        cursor.close()
        connection.close()
    
def convert_database_to_csv(url, schema='public', output_dir = '/workspace/cache'):
    connection = psycopg2.connect(url)
    cursor = connection.cursor()
    tables = get_postgres_tables(url, schema)
    # import pdb; pdb.set_trace()
    for table in tables:
        sql = f" \COPY {schema}.{table} TO  '/workspace/cache/rides.csv' WITH CSV HEADER;"
        cursor.execute(sql)


def parse_xml(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    xml_schema = {}
    for table in root.findall('.//table'):
        table_name = table.get('name')
        columns = [(column.get('name'), column.get('type')) for column in table.findall('.//column')]
        xml_schema[table_name] = columns

    return xml_schema

def compare_schemas(postgres_schema, xml_schema):
    for table_name, columns in xml_schema.items():
        if table_name not in postgres_schema:
            print(f"Table '{table_name}' not found in the PostgreSQL schema.")
            continue

        postgres_columns = postgres_schema[table_name]
        if set(columns) != set(postgres_columns):
            print(f"Schema mismatch for table '{table_name}':")
            print(f"PostgreSQL Schema: {postgres_columns}")
            print(f"XML Schema: {columns}")
        else:
            print(f"Table '{table_name}' schema matches.")            


if __name__ == "__main__":

    url = 'postgresql://xlanglab:123456@127.0.0.1:12001/xlangdb'
    # answer = get_postgres_tables(url, "bike_rental")
    # print(answer)
    # answer = get_postgres_columns(url, "date_dim","bike_rental")
    # print(answer)
    # answer = execute_query(url, "SELECT * FROM bike_rental.date_dim;")
    # print(answer)
    # convert_database_to_csv(url, schema='bike_rental')
    # # Path to the XML file
    # xml_file_path = 'path/to/your/xml/file.xml'

    # # Get PostgreSQL schema
    postgres_schema = get_postgres_schema(url)
    print(postgres_schema)

    # # Parse XML schema
    # xml_schema = parse_xml(xml_file_path)

    # # Compare schemas
    # compare_schemas(postgres_schema, xml_schema)
    
    # import os
    # for file in os.listdir("/Users/leifangyu/workspace/DataAgentBench/benchmark/source/load001/csv"):
    #     import pdb; pdb.set_trace()
        
    


# postgresql://xlanglab:123456@127.0.0.1:12001/xlangdb?currentSchema=你的schema名
