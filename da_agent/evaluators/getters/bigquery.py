import json
from google.cloud import bigquery
from google.oauth2 import service_account
import os
import logging

logger = logging.getLogger("da_agent.getters.bigquery")

def get_bigquery_table_to_csv(env, config):
    """ Given the project name or index, dataset id and table id, return the table content if found, otherwise return None.
    @args:
        env(dict): the environment dictionary
        config(dict): the configuration dictionary
            - config_file(str): the path to the GCP config file
            - project_name(str): the project name
            - project_index(int): the project index, either project_name or project_index must be specified
            - dataset_id(str): the dataset id
            - table_id(str): the table id
            - dest(str): the path to the output file, combined with env.cache_dir
    @return:
        filepath: the filepath containing target db content if found, otherwise None
    """

    config_file = config.get('config_file', 'evaluation_examples/settings/google/gcp_config.json')
    gcp_config = json.load(open(config_file, 'r'))
    if 'project_name' in config:
        prj_name = config['project_name']
        for proj in gcp_config:
            if prj_name == proj['project_name']:
                gcp_config = proj
                break
        else:
            raise ValueError(f'[ERROR]: The specified project name {prj_name} is not found in the GCP config file!')
    else:
        assert 'project_index' in config, "Must specify either project_name or project_index in config!"
        gcp_config = gcp_config[config['project_index']]
    keyfile_path, project_id = gcp_config['keyfile_path'], gcp_config['project_id']
    credentials = service_account.Credentials.from_service_account_file(keyfile_path)
    client = bigquery.Client(project=project_id, credentials=credentials)

    dataset_id, table_id = config['dataset_id'], config['table_id']
    try:
        dataset_ref = f'{project_id}.{dataset_id}'
        list(client.list_tables(dataset_ref))
    except:
        client.close()
        logger.error(f'[ERROR]: Failed to get the dataset {dataset_ref} from bigquery!')
        raise FileNotFoundError(f'[ERROR]: Failed to get the dataset {dataset_ref} from bigquery!')
        return

    try:
        table_ref = f'{project_id}.{dataset_id}.{table_id}'
        client.get_table(table_ref)
    except:
        logger.error(f'[ERROR]: Failed to get the table {table_ref} from bigquery!')
        raise FileNotFoundError(f'[ERROR]: Failed to get the table {table_ref} from bigquery!')
        client.close()
        return
    
    mnt_dir = getattr(env, "mnt_dir")
    work_dir = getattr(env, "work_dir")
    output_file = config['dest'].replace(work_dir, mnt_dir)
    if os.path.exists(output_file):
        os.remove(output_file)
    
    schema = config.get('schema', '*')
    if schema != '*':
        schema = ', '.join(config['schema'])
    query = f"SELECT {schema} FROM {project_id}.{dataset_id}.{table_id}"
    
    try:
        job = client.query(query)
        df = job.to_dataframe()
        df.to_csv(output_file, index=False)
    except Exception as e:
        logger.error(f'[ERROR]: Failed to get the table content from bigquery, query is {query}. Error: {e}')

    return output_file