import argparse
import datetime
import json
import logging
import os
import random
import sys

from tqdm import tqdm

from spider2.envs.spider2 import Spider2Env
from llm_agents.agent import PromptAgent


#  Logger Configs {{{ #
logger = logging.getLogger("spider2")
logger.setLevel(logging.DEBUG)

datetime_str: str = datetime.datetime.now().strftime("%Y%m%d@%H%M%S")

file_handler = logging.FileHandler(os.path.join("logs", "normal-{:}.log".format(datetime_str)), encoding="utf-8")
debug_handler = logging.FileHandler(os.path.join("logs", "debug-{:}.log".format(datetime_str)), encoding="utf-8")
stdout_handler = logging.StreamHandler(sys.stdout)
sdebug_handler = logging.FileHandler(os.path.join("logs", "sdebug-{:}.log".format(datetime_str)), encoding="utf-8")

file_handler.setLevel(logging.INFO)
debug_handler.setLevel(logging.DEBUG)
stdout_handler.setLevel(logging.INFO)
sdebug_handler.setLevel(logging.DEBUG)

formatter = logging.Formatter(
    fmt="\x1b[1;33m[%(asctime)s \x1b[31m%(levelname)s \x1b[32m%(module)s/%(lineno)d-%(processName)s\x1b[1;33m] \x1b[0m%(message)s")
file_handler.setFormatter(formatter)
debug_handler.setFormatter(formatter)
stdout_handler.setFormatter(formatter)
sdebug_handler.setFormatter(formatter)

stdout_handler.addFilter(logging.Filter("spider2"))
sdebug_handler.addFilter(logging.Filter("spider2"))

logger.addHandler(file_handler)
logger.addHandler(debug_handler)
logger.addHandler(stdout_handler)
logger.addHandler(sdebug_handler)
#  }}} Logger Configs # 



def config() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run end-to-end evaluation on the benchmark"
    )
    
    parser.add_argument("--max_steps", type=int, default=15)
    
    parser.add_argument("--max_trajectory_length", type=int, default=5)
    parser.add_argument("--test_config_base_dir", type=str, default="evaluation_examples")
    
    parser.add_argument("--model", type=str, default="gpt-4")
    parser.add_argument("--temperature", type=float, default=1.0)
    parser.add_argument("--top_p", type=float, default=0.9)
    parser.add_argument("--max_tokens", type=int, default=1500)
    parser.add_argument("--stop_token", type=str, default=None)
    
    # example config
    parser.add_argument("--domain", type=str, default="all")
    parser.add_argument("--test_all_meta_path", type=str, default="evaluation_examples/test_all.json")

    # logging related
    parser.add_argument("--result_dir", type=str, default="./results")
    args = parser.parse_args()

    return args






def test(
    args: argparse.Namespace,
    test_all_meta: dict = None
) -> None:
    scores = []
    max_steps = args.max_steps
    
    # log args
    logger.info("Args: %s", args)
    
    cfg_args = \
    {
        "max_steps": args.max_steps,
        "max_trajectory_length": args.max_trajectory_length,
        "model": args.model,
        "temperature": args.temperature,
        "top_p": args.top_p,
        "max_tokens": args.max_tokens,
        "result_dir": args.result_dir
    }
    
    agent = PromptAgent(
        model=args.model,
        max_tokens=args.max_tokens,
        top_p=args.top_p,
        temperature=args.temperature,
        max_trajectory_length=args.max_trajectory_length
    )
    
    
    data_path = './evaluation_examples/examples/ga4/ga001.json'
    with open(data_path, "r") as f:
        data = json.load(f)
    container_name = 'spider2'
    data['init_args']['name'] = container_name
    
    env = Spider2Env(
        task_config=data,
        cache_dir="./cache"
    )
    
    agent.set_env(env)
    
    
    logger.info('Task input:' + data['instruction'])
    done = False
    step_idx = 0
    obs = "you are in the folder."
    while not done and step_idx < max_steps:
        
        lines = []
        while True:
            line = input("请输入内容（输入'end'结束）: ")
            if line == 'end':
                break
            lines.append(line)

        # 将输入的内容存储为一个字符串，并在每行之间添加换行符
        action = '\n'.join(lines)

        action = agent.parse_action(action)
        

        action_timestamp = datetime.datetime.now().strftime("%Y%m%d@%H%M%S")

        logger.info("Step %d: %s", step_idx + 1, action)


        obs, done = agent.step(action)

        if done:
            logger.info("The task is done.")
            break
        step_idx += 1

    result = env.evaluate()
    logger.info("Result: %.2f", result)
    scores.append(result)
    print(result)
    
    logger.info(f"Average score: {sum(scores) / len(scores)}")

if __name__ == '__main__':
    args = config()
    
    # with open(args.test_all_meta_path, "r") as f:
    #     test_all_meta = json.load(f)
        
        
    # if args.domain != "all":
    #     test_all_meta = {args.domain: test_all_meta[args.domain]}
        
    # test_file_list = test_all_meta
    
    test(args)