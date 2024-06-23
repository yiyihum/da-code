#coding=utf8
import json, logging, platform
from google.cloud import bigquery
from google.oauth2 import service_account
from google.cloud.bigquery.dataset import DatasetListItem
from typing import List, Tuple, Union


logger = logging.getLogger("desktopenv.setup")


def bigquery_empty_project(client: bigquery.Client, **config):
    """ Empty all the resources in the specified GCP project, including jobs, datasets, routines, models, tables, etc.
    """
    for job in client.list_jobs():
        client.cancel_job(job)
        client.delete_job_metadata(job)
    for dataset in client.list_datasets():
        for routine in client.list_routines(dataset):
            client.delete_routine(routine, not_found_ok=True)
        for model in client.list_models(dataset):
            client.delete_model(model, not_found_ok=True)
        client.delete_dataset(dataset, delete_contents=True)
    return




BIGQUERY_INIT_FUNCTIONS = {
    "empty": bigquery_empty_project
}


def bigquery_init_setup(controller, **config):
    """ Setup the BigQuery client and perform environment setup. Please ensure that BigQuery API is enabled for the specified project. Arguments for config dict:
    @args:
        config_file(str): the path to the GCP keyfile, default is 'evaluation_examples/settings/google/gcp_config.json'
        project_name(str): the GCP name to search in the config file, if not provided, use project_index to get the project
        project_index(int): the index of the project in the config file, either this field or project_name must be provided
        actions(list): the list of actions to perform, each action is one dict with `type` field chosen from ['empty']:
        (No perfect documentation found, please refer to bigquery source codes for more details)
            - empty: empty the entire GCP, including datasets, jobs, routines, models, tables, etc.
            - create_table: create a dataset and a table in it, with optional schema and data fields
            - copy_keyfile: copy the keyfile from host to guest
    """
    config_file = config.get('config_file', 'evaluation_examples/settings/google/gcp_config.json')
    if platform.system() == 'Windows':
        config_file = config_file.replace('/', '\\')
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

    actions = config.get('actions', [])
    if len(actions) == 0:
        logger.error('[ERROR]: No action is specified in the `actions` field!')
        return

    for action in actions:
        action_type = action.pop('type', 'empty')
        action['controller'], action['project_id'], action['keyfile_path'] = controller, project_id, keyfile_path
        try:
            BIGQUERY_INIT_FUNCTIONS[action_type](client, **action)
        except Exception as e:
            logger.error(f'[ERROR]: failed in bigquery_init function when call action `{action_type}`')

    client.close()
    return
