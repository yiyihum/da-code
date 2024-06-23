#coding=utf8
import os
from .file import get_vm_file


def get_dbt_profiles(env, config: Dict[str, str]) -> str:
    """ Download dbt profiles.yml file from VM, search all possible paths and return the first one found.
    Paths include:
        config (Dict[str, Any]):
            dirs (List[str]): a list of possible dirs to search profiles.yml, if the path starts with a '$', it will be treated as an environment variable
            dest (str): local file name of the downloaded file
        working, default and environment variable DBT_PROFILES_DIR
    """
    for fp in config["dirs"]:
        if fp.startswith('$'):
            fp = get_vm_command_line(env, {"command": ["/bin/bash", "-c", f"echo \"{fp}\""]})
            if type(fp) == str and fp.strip() != "":
                file = get_vm_file(env, {"path": fp.strip() + '/profiles.yml', "dest": config["dest"]})
                if file is not None:
                    return file
        else:
            file = get_vm_file(env, {"path": fp + '/profiles.yml', "dest": config["dest"]})
            if file is not None:
                return file

    return None



