import logging
from typing import Dict
import docker
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append("/Users/leifangyu/workspace/DataAgentBench/environment")
sys.path.append("/Users/leifangyu/workspace/DataAgentBench")

    
def get_docker_script_output(env, config: Dict[str, str]):
    env.setup_controller._download_setup([{"url": config["url"], "path": config["dest"]}])
    env.setup_controller._execute_setup(command=f"chmod a+x {config['dest']}") 
    response = env.setup_controller._execute_setup(command=f"bash {config['dest']}")
    env.setup_controller._execute_setup(command=f"rm -f {config['dest']}")
    return response



