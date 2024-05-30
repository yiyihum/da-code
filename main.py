#coding=utf8
import json, logging, os, sys
from typing import Type
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from rich.logging import RichHandler
# from agents.agent_base import AgentBase
# from agents.llm_utils import LLMWrapper
# from agents.prompt_utils import PromptTemplate, ReActPrompt, PlanSolvePrompt
# from agents.memory_utils import MemoryBase
# from environment.env_base import DataAgentEnv
# from environment.evaluation import evaluate
import docker
import argparse
import pandas as pd
# from evaluation.eval_utils import *
import time
import subprocess

from spider2.envs.spider2 import Spider2Env


# Set up logger
handler = RichHandler(show_time=False)
handler.setLevel(logging.DEBUG)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(handler)

max_trials: int = 1
max_turns: int = 1

# prompt: PromptTemplate = ReActPrompt() #PromptTemplate(), PlanSolvePrompt()

# memory: MemoryBase = MemoryBase(max_trials=3)

def human_agent():
    """
    Runs the Gym environment with human input.
    """    
    data_path = './evaluation_examples/examples/datavisualization/datavisualization000.json'
    with open(data_path, "r") as f:
        data = json.load(f)

    container_name = 'spider2'
    data['init_args']['name'] = container_name

    mnt_dir = '/Users/stewiepeter/Desktop/VsProjects/VaftBench/dabench/benchmark/output/gpt-4-20240530-144050'

    os.makedirs(os.path.join(mnt_dir, 'dabench'), exist_ok=True)
    env = Spider2Env(
        task_config=data,
        env_config=data,
        cache_dir="./cache",
        mnt_dir= mnt_dir
    )
    
    logger.info('Task input:' + data['instruction'])

    input("Press Enter to start human operation...")
    human_start_time = time.time()
    input("Press Enter to finish human operation.")
    print("Time elapsed of human operation: %.2f" % (time.time() - human_start_time))

    while True:
        score = env.post_process()
        print(score)
        import pdb; pdb.set_trace()

        


if __name__ == "__main__":
    human_agent()