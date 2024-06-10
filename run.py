import argparse
import datetime
import json
import logging
import os
import random
import sys

from tqdm import tqdm

from spider2.envs.spider2 import Spider2Env
from spider2.agent.agents import PromptAgent


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
    
    parser.add_argument("--max_steps", type=int, default=20)
    
    parser.add_argument("--max_memory_length", type=int, default=15)
    parser.add_argument("--suffix", '-s', type=str, default="test")
    
    parser.add_argument("--model", type=str, default="azure")
    parser.add_argument("--temperature", type=float, default=0.0)
    parser.add_argument("--top_p", type=float, default=0.9)
    parser.add_argument("--max_tokens", type=int, default=1500)
    parser.add_argument("--stop_token", type=str, default=None)
    
    # example config
    parser.add_argument("--domain", type=str, default="all")
    parser.add_argument("--test_all_meta_path","-t",type=str, default="benchmark/configs/ML.jsonl")
    parser.add_argument("--example_index", "-i", type=str, default="all", help="index range of the examples to run, e.g., '0-10', '2,3', 'all'")
    parser.add_argument("--example_name", "-n", type=str, default="", help="name of the example to run")
    parser.add_argument("--skip_existing", action="store_true", default=False)
    parser.add_argument("--retry_failed", action="store_true", default=False)


    # output related
    parser.add_argument("--output_dir", type=str, default="./benchmark/output")
    args = parser.parse_args()

    return args



def test(
    args: argparse.Namespace,
    test_all_meta: dict = None
) -> None:
    scores = []
    
    # log args
    logger.info("Args: %s", args)
    
    cfg_args = \
    {
        "max_steps": args.max_steps,
        "max_memory_length": args.max_memory_length,
        "model": args.model,
        "temperature": args.temperature,
        "top_p": args.top_p,
        "max_tokens": args.max_tokens,
    }

    if args.suffix == "":
        experiment_id = args.model + "-" +datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    else:
        experiment_id = args.model + "-" + args.suffix

    env_config = \
    {
        "image_name": "dabench-image",
        "init_args": {
            "name": experiment_id,
            "work_dir": "/workspace",
        }
    }
    
    agent = PromptAgent(
        model=args.model,
        max_tokens=args.max_tokens,
        top_p=args.top_p,
        temperature=args.temperature,
        max_memory_length=args.max_memory_length,
        max_steps=args.max_steps,
    )
    
    ## load task configs
    assert os.path.exists(args.test_all_meta_path) and args.test_all_meta_path.endswith(".jsonl"), f"Invalid test_all_meta_path, must be a valid jsonl file: {args.test_all_meta_path}"
    with open(args.test_all_meta_path, "r") as f:
        task_configs = [json.loads(line) for line in f]
    if args.example_name != "":
        task_configs = [task for task in task_configs if args.example_name in task["id"]]
    else:
        if args.example_index != "all":
            if "-" in args.example_index:
                start, end = map(int, args.example_index.split("-"))
                task_configs = task_configs[start:end]
            else:
                indices = list(map(int, args.example_index.split(",")))
                task_configs = [task_configs[i] for i in indices]
    
    # TODO: record the task state
    # save all setting to output_dir
    # delete container after finish
    for task_config in task_configs:
        instance_id = experiment_id +"/"+ task_config["id"]
        output_dir = os.path.join(args.output_dir, instance_id)
        result_json_path =os.path.join(output_dir, "dabench/result.json")
        if args.skip_existing and os.path.exists(result_json_path):
            logger.info("Skipping %s", instance_id)
            continue
        if args.retry_failed and os.path.exists(result_json_path):
            with open(result_json_path, "r") as f:
                result = json.load(f)
                if result["finished"]:
                    logger.info("Skipping %s", instance_id)
                    continue
            logger.info("Retrying %s", instance_id)
            
        if os.path.exists(output_dir):
            os.system(f"rm -rf {output_dir}")
            logger.info("Removed existing %s", output_dir)

        os.makedirs(output_dir, exist_ok=True)

        env_config["init_args"]["name"] = experiment_id +"-"+ task_config["id"]
        env = Spider2Env(
            env_config=env_config,
            task_config=task_config,
            cache_dir="./cache",
            mnt_dir=output_dir
        )
    
        agent.set_env_and_task(env)
    
        logger.info('Task input:' + task_config['instruction'])
        done, result_output = agent.run()
        trajectory = agent.get_trajectory()

        os.makedirs(os.path.join(output_dir, "dabench"), exist_ok=True)
        result_files = env.post_process()
        dabench_result = {"finished": done, "steps": len(trajectory["trajectory"]),
                           "result": result_output,"result_files": result_files, **trajectory}
        with open(os.path.join(output_dir, "dabench/result.json"), "w") as f:
            json.dump(dabench_result, f, indent=2)
        
        logger.info("Finished %s", instance_id)
        env.close()




if __name__ == '__main__':
    args = config()
    
    test(args)