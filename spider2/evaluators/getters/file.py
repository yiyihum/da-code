import os
from typing import Dict, List, Set
from typing import Optional, Any, Union

import requests
import csv




def get_cloud_file(env, config: Dict[str, Any]) -> Union[str, List[str]]:
    """
    Config:
        path (str|List[str]): the url to download from
        dest (str|List[str])): file name of the downloaded file
        multi (bool) : optional. if path and dest are lists providing
          information of multiple files. defaults to False
        gives (List[int]): optional. defaults to [0]. which files are directly
          returned to the metric. if len==1, str is returned; else, list is
          returned.
    """
    mnt_dir = getattr(env, "mnt_dir")
    work_dir = getattr(env, "work_dir")
    
    if not config.get("multi", False):
        paths: List[str] = [config["path"]]
        dests: List[str] = [config["dest"]]
    else:
        paths: List[str] = config["path"]
        dests: List[str] = config["dest"]
    cache_paths: List[str] = []

    gives: Set[int] = set(config.get("gives", [0]))

    for i, (p, d) in enumerate(zip(paths, dests)):
        _path = os.path.join(d.replace(work_dir, mnt_dir))

        cache_paths.append(_path)


        url = p
        response = requests.get(url, stream=True)
        response.raise_for_status()

        with open(_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)

    return cache_paths[0] if len(cache_paths)==1 else cache_paths



def get_docker_file(env, config: Dict[str, Any]) -> Union[Optional[str], List[Optional[str]]]:
    """
    Config:
        path (str): absolute path on the VM to fetch
        dest (str): file name of the downloaded file
        multi (bool) : optional. if path and dest are lists providing
          information of multiple files. defaults to False
        gives (List[int]): optional. defaults to [0]. which files are directly
          returned to the metric. if len==1, str is returned; else, list is
          returned.
    """

    mnt_dir = getattr(env, "mnt_dir")
    work_dir = getattr(env, "work_dir")
    if not config.get("multi", False):
        paths: List[str] = [config["path"]]
    else:
        paths: List[str] = config["path"]
    cache_paths = []
    

    
    for _path in paths:
        cache_paths.append(_path.replace(work_dir, mnt_dir))

    return cache_paths[0] if len(cache_paths)==1 else cache_paths


def get_local_file(env, config: Dict[str, Any]) -> Union[Optional[str], List[Optional[str]]]:
    if not config.get("multi", False):
        paths: List[str] = [config["path"]]
    else:
        paths: List[str] = config["path"]
    cache_paths = []    
    for _path in paths:
        cache_paths.append(_path)

    return cache_paths[0] if len(cache_paths)==1 else cache_paths



if __name__ == "__main__":
    pass