import logging
import os, json
from typing import Callable, Any
from typing import List, Dict, Union
from pathlib import Path
import sys, jsonlines
here=Path(__file__).absolute()
sys.path.append(str(here.parent))
import metrics
from tqdm import tqdm
from spider2.envs.utils import timeout
import re

Metric = Callable[[Any, Any], float]

class Evaluator:

    def __init__(self, output_dir: str, gold_dir: str, timeout_second: int = 10):
        self.output_dir = output_dir
        self.gold_dir = gold_dir
        self.timeout_second = timeout_second

    def get_result_file(self, results: List, dir: str, isgold: bool):
        results = results if isinstance(results, list)\
            else [results]
        result_files = []
        for result in results:
            multi = result.get("multi", False)
            files = result['file'] if isinstance(result['file'], list) \
                else [result['file']]
            if multi:
                files = [os.path.join(dir, file) for file in files] if not isgold \
                    else [os.path.join(dir, os.path.basename(file)) for file in files]
                result_files.append(files)
            else:
                for file in files:
                    file = file if not isgold else os.path.basename(file)
                    result_files.append(os.path.join(dir, file))
        return result_files

    def _get_eval_config_info(self, eval_config: Dict[str, Any]):
        # evaluator dict
        # func -> metric function string, or list of metric function strings
        # conj -> conjunction of multiple metrics if func is a list with length > 1, "and"/"or"
        # result -> result getter config, or list of result getter configs
        # expected (optional) -> expected getter config, or list of expected getter configs
        # options (optional) -> metric options, or list of metric options
        # if func is a str list, then result, expected (if exists), options (if exists) should also be lists of the same length
        # even if one of the metrics does not need expected or options field, it should be included in the list with None
        # self.evaluator = task_config["evaluator"]
        id = eval_config['id']
        output_id_dir = os.path.join(self.output_dir, id)
        gold_id_dir = os.path.join(self.gold_dir, id)
        config = eval_config.get('config', {})
        metric: Metric = [getattr(metrics, func) for func in eval_config["func"]] \
            if isinstance(eval_config["func"], list)\
            else [getattr(metrics, eval_config["func"])]
        metric_conj: str = eval_config.get("conj", "avg")  # take conjunction of multiple metrics
        expected = eval_config['result'] if isinstance(eval_config['result'], list) \
            else [eval_config['result']]
        # expected = eval_config.get('expected', [])
        # if expected == []:
        # expected = result    
        
        output_results = self._get_result_file_from_json(output_id_dir, is_plot=("dabench/plot.json" in expected))
        if not output_results:
            output_results = self.get_result_file(expected, dir=output_id_dir, isgold=False)
        gold_results = self.get_result_file(expected, dir=gold_id_dir, isgold=True)
        metric_options: Union[List[Dict[str, Any]], Dict[str, Any]] = \
            [opt if opt else {} for opt in eval_config["options"]] \
            if isinstance(eval_config.get("options", {}), list) \
            else eval_config["options"] \
            if "options" in eval_config.keys() \
            else [{}] * len(metric) \
            if isinstance(metric, list) \
            else {}
  
        assert (not isinstance(eval_config["func"], list)
            or (len(metric) == len(output_results) == len(gold_results) == len(
                metric_options)))
        
        return id, config, metric, metric_conj, metric_options, output_results, gold_results

    def _get_result_file_from_json(self, output_id_dir, is_plot=False):
        result_file = os.path.join(output_id_dir, 'dabench', 'result.json')
        if not os.path.exists(result_file):
            print(f"File {result_file} not found")
            return []
        with open(result_file, 'r') as f:
            result = json.load(f)
            result_file = result['result']
                # 正则表达式匹配文件路径和文件名，路径和文件名可以包含字母、数字、下划线、破折号和点
            pattern = r'\b(?:[\w/\-_]+/)?([\w\-_]+(\.\w+)+)\b'
            # 使用findall找到所有匹配的文件名
            filenames = re.findall(pattern, result_file)
            if not filenames:
                print(f"File not found : {result_file}; dir: {output_id_dir}")
                return []
            # findall返回的是元组列表，我们只需要文件名部分
            filenames = [filename[0] for filename in filenames]
            result_file = [os.path.join(output_id_dir, file) for file in filenames]
        if is_plot:
            result_file += [os.path.join(output_id_dir,"dabench/plot.json"), os.path.join(output_id_dir,"dabench/result.npy")]
        return result_file
    
    def evaluate(self, env_config: Dict|str):
        """
        Evaluate task
        """
        if isinstance(env_config, str):
            if not os.path.exists(env_config) or not os.path.isfile(env_config):
                raise ValueError('File Path Error: Please provide a right file path')
            if env_config.endswith('.json'):
                with open(env_config, 'r') as f:
                    env_configs = json.load(f)
            elif env_config.endswith('.jsonl'):
                with jsonlines.open(env_config, 'r') as js:
                    env_configs = [config_eval for config_eval in js]
            else:
                raise ValueError('File Type Error: Please Upload json or jsonl file')
            env_configs = env_configs if isinstance(env_configs, list) else [env_configs]
        elif isinstance(eval_config, dict):
            env_configs = [env_config] 
       
        eval_results = []
        pbar = tqdm(total=len(env_configs))

        for eval_config in env_configs:
            try:
                with timeout(self.timeout_second,"Action execution time exceeded!"):
                    id, config, metrics, metric_conj, metric_options, output_results, gold_results = \
                        self._get_eval_config_info(eval_config)
                    pbar.set_description(f"Processing Task id: {id}")
                    pbar.update(1)
                    if metrics == "infeasible":
                        return 0
                    scores = []
                    info = []
                    for idx, metric in enumerate(metrics):
                        try:
                            output_result = output_results[idx]
                            gold_result = gold_results[idx]
                            if config:
                                config_copy = {"config": config}
                                metric_options[idx].update(config_copy)
                            result = metric(output_result, gold_result,**metric_options[idx])
                        except FileNotFoundError:
                            logging.error("File not found!")
                            scores.append(0.0)
                            continue
                        if isinstance(result, dict):
                            scores.append(result.get('score', 0.0))
                            output_result = output_result if isinstance(output_result, list) else [output_result]
                            result['file'] = [os.path.basename(file) for file in output_result]
                            info.append(result)
                        else:
                            scores.append(result)
            except Exception as e:
                output_result = output_result if isinstance(output_result, list) else [output_result]
                logging.error(f"Error in task {id}: {e}")
                scores.append(0.0)
                info.append({"score": 0.0, "errors": [str(e)], 'file': [os.path.basename(file) for file in output_result]})

            if metric_conj == 'avg':
                eval_results.append({"id": id, "total_score": sum(scores) / len(scores), 'info': info})
            elif metric_conj == 'max':
                eval_results.append({"id": id, "total_score": max(scores),'info': info})
            elif metric_conj == 'min':
                eval_results.append({"id": id, "total_score": min(scores),'info': info})
            elif metric_conj == 'and':
                eval_results.append({"id": id, "total_score": float(all(score!= 0 for score in scores)),'info': info})
            elif metric_conj == 'or':
                eval_results.append({"id": id, "total_score": float(any(score!= 0 for score in scores)),'info': info})
        return eval_results