import logging
from typing import Dict
import docker
import sys, os
import psycopg2




def get_postgre_files(env, config):
    schema = config['schema']
    dest_path = config['dest']
    

    create_bash = f"""
    table_names=$(psql -h localhost -U xlanglab -d xlangdb -t -c "SELECT table_name FROM information_schema.tables WHERE table_schema = '{schema}';")

    for table_name in $table_names
    do
        export_file="{dest_path}/${{table_name}}.csv"
        psql -h localhost -U xlanglab -d xlangdb -c "\\COPY {schema}.$table_name TO '$export_file' WITH CSV HEADER;"
    done
    """

    env.setup_controller._execute_setup(command=create_bash)
    
    
    mnt_dir = getattr(env, "mnt_dir")
    work_dir = getattr(env, "work_dir")
    postgre_path = os.path.join(dest_path.replace(work_dir, mnt_dir))
    
    return postgre_path
    