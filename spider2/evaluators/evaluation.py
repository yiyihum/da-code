import logging
import os, json
from typing import Callable, Any
from typing import List, Dict, Union
from pathlib import Path
import sys
here=Path(__file__).absolute()
sys.path.append(str(here.parent))
import metrics

Metric = Callable[[Any, Any], float]

class Evaluator:

    def __init__(self, output_dir: str, gold_dir: str):
        self.output_dir = output_dir
        self.gold_dir = gold_dir

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
        assert os.path.exists(output_id_dir), f'{output_id_dir} does not exist'
        assert os.path.exists(gold_id_dir), f'{gold_id_dir} does not exist'
        config = eval_config.get('config', {})
        metric: Metric = [getattr(metrics, func) for func in eval_config["func"]] \
            if isinstance(eval_config["func"], list)\
            else [getattr(metrics, eval_config["func"])]
        metric_conj: str = eval_config.get("conj", "and")  # take conjunction of multiple metrics
        result = eval_config['result'] if isinstance(eval_config['result'], list) \
            else [eval_config['result']]
        output_results = self.get_result_file(result, dir=output_id_dir, isgold=False)
        gold_results = self.get_result_file(result, dir=gold_id_dir, isgold=True)
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
        
        return metric, metric_conj, metric_options, output_results, gold_results
    
    def evaluate(self, env_config: Dict|str):
        """
        Evaluate task
        """
        if isinstance(env_config, str):
            with open(env_config, 'r') as f:
                env_config = json.load(f)
        metrics, metric_conj, metric_options, output_results, gold_results = \
            self._get_eval_config_info(env_config)
        if metrics == "infeasible":
           return 0
        results = []
        info = []
        for idx, metric in enumerate(metrics):
            try:
               output_result = output_results[idx]
               gold_result = gold_results[idx]
               metric: int = metric(output_result, gold_result,
                **metric_options[idx])
            except FileNotFoundError:
                logging.error("File not found!")
                results.append(0.0)
                continue
            if isinstance(metric, dict):
                results.append(metric.pop('score', 0.0))
                info.append(metric)
            else:
                results.append(metric)

        if metric_conj == 'and':
            return sum(results) / len(results), info
        elif metric_conj == 'or':
            return max(results), info
        
      
    
 