import argparse
import datetime
import json
import logging
import os
import random
import sys

from tqdm import tqdm

from da_agent.envs.da_agent import DA_Agent_Env
from da_agent.agent.agents import PromptAgent


#  Logger Configs {{{ #
logger = logging.getLogger("da_agent")
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

stdout_handler.addFilter(logging.Filter("da_agent"))
sdebug_handler.addFilter(logging.Filter("da_agent"))

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
    parser.add_argument("--suffix", '-s', type=str, default="")
    
    parser.add_argument("--model",'-m',type=str, default="gpt-4o")
    parser.add_argument("--temperature", type=float, default=0.0)
    parser.add_argument("--top_p", type=float, default=0.9)
    parser.add_argument("--max_tokens", type=int, default=1500)
    parser.add_argument("--stop_token", type=str, default=None)
    
    # example config
    parser.add_argument("--task_config","-t", type=str, default="da_code/configs/task/examples.jsonl")
    parser.add_argument("--source_dir", type=str, default="da_code/source")
    parser.add_argument("--example_index", "-i", type=str, default="all", help="index range of the examples to run, e.g., '0-10', '2,3', 'all'")
    parser.add_argument("--example_name", "-n", type=str, default="", help="name of the example to run")
    parser.add_argument("--overwriting", action="store_true", default=False)
    parser.add_argument("--retry_failed", action="store_true", default=False)

    # output related
    parser.add_argument("--output_dir", type=str, default="output")
    args = parser.parse_args()

    return args



def test(
    args: argparse.Namespace,
    test_all_meta: dict = None
) -> None:
    scores = []
    
    # log args
    logger.info("Args: %s", args)

    import uuid
    
    # 先检查是否已有相同 suffix 的实验在输出目录中
    existing_experiment_id = None
    if args.suffix != "":
        # 尝试查找已存在的具有相同 suffix 前缀的实验
        expected_prefix = args.model.split("/")[-1] + "-" + args.suffix + "-"
        if os.path.exists(args.output_dir):
            for item in os.listdir(args.output_dir):
                if item.startswith(expected_prefix) and os.path.isdir(os.path.join(args.output_dir, item)):
                    existing_experiment_id = item
                    logger.info("Reusing existing experiment ID: %s", existing_experiment_id)
                    break
    
    if existing_experiment_id:
        experiment_id = existing_experiment_id
    else:
        # 如果没有找到，创建新的
        if args.suffix == "":
            logger.warning("No suffix is provided, the experiment id will be the model name.")
            experiment_id = args.model.split("/")[-1] + "-" + uuid.uuid4().hex[:8]
        else:
            experiment_id = args.model.split("/")[-1] + "-" + args.suffix + "-" + uuid.uuid4().hex[:8]
        
    env_config = \
    {
        "image_name": "da_agent-image",
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
    assert os.path.exists(args.task_config) and args.task_config.endswith(".jsonl"), f"Invalid task_config, must be a valid jsonl file: {args.task_config}"
    with open(args.task_config, "r", encoding="utf-8") as f:
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
    
    for task_config in task_configs:
        instance_id = experiment_id +"/"+ task_config["id"]
        output_dir = os.path.join(args.output_dir, instance_id)
        result_json_path =os.path.join(output_dir, "dabench/result.json")
        
        # 检查是否已经有完成的结果（包括其他实验ID的运行）
        skip_task = False
        existing_result = None
        existing_result_path = None
        
        if not args.overwriting:
            # 首先检查当前路径
            if os.path.exists(result_json_path):
                with open(result_json_path, "r") as f:
                    existing_result = json.load(f)
                existing_result_path = result_json_path
            else:
                # 查找是否有其他实验已经完成了这个任务
                # 获取模型名称（从实验ID中提取）
                model_name = experiment_id.split("-")[0]
                # 在当前输出目录的父目录中搜索
                parent_dir = os.path.dirname(output_dir)
                if os.path.exists(parent_dir):
                    for exp_dir in os.listdir(parent_dir):
                        exp_path = os.path.join(parent_dir, exp_dir)
                        if os.path.isdir(exp_path):
                            task_result_path = os.path.join(exp_path, task_config["id"], "dabench/result.json")
                            if os.path.exists(task_result_path):
                                try:
                                    with open(task_result_path, "r") as f:
                                        result = json.load(f)
                                        existing_result = result
                                        existing_result_path = task_result_path
                                        break
                                except:
                                    pass
            
            # 决定是否跳过
            if existing_result:
                if args.retry_failed:
                    # 如果设置了 retry_failed，只有成功的任务才跳过
                    if existing_result.get("finished") and not "FAIL" in existing_result.get("result", "") and not "error" in existing_result.get("result", "").lower():
                        logger.info("Skipping %s (already succeeded in %s)", instance_id, existing_result_path)
                        skip_task = True
                    else:
                        logger.info("Retrying %s (failed previously in %s)", instance_id, existing_result_path)
                else:
                    # 否则，任何已存在的结果都跳过
                    logger.info("Skipping %s (already exists in %s)", instance_id, existing_result_path)
                    skip_task = True
        
        if skip_task:
            continue
            
        if os.path.exists(result_json_path):
            logger.info("Overwriting %s", instance_id)
        else:
            logger.info("Running %s", instance_id)
            
        if os.path.exists(output_dir):
            os.system(f"rm -rf {output_dir}")
            logger.info("Removed existing %s", output_dir)

        os.makedirs(output_dir, exist_ok=True)

        env_config["init_args"]["name"] = experiment_id +"-"+ task_config["id"]
        env = DA_Agent_Env(
            env_config=env_config,
            task_config=task_config,
            source_dir=args.source_dir,
            cache_dir="./cache",
            mnt_dir=output_dir
        )
    
        agent.set_env_and_task(env)
    
        logger.info('Task input:' + task_config['instruction'])
        done, result_output = agent.run()
        trajectory = agent.get_trajectory()

        os.makedirs(os.path.join(output_dir, "dabench"), exist_ok=True)
        result_files = env.post_process()
        
        # Clean up source files before saving results
        env._cleanup_source_files()
        
        dabench_result = {"finished": done, "steps": len(trajectory["trajectory"]),
                           "result": result_output,"result_files": result_files, **trajectory}
        with open(os.path.join(output_dir, "dabench/result.json"), "w") as f:
            json.dump(dabench_result, f, indent=2)
        
        logger.info("Finished %s", instance_id)
        env.close()




if __name__ == '__main__':
    args = config()
    
    test(args)