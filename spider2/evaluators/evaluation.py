import logging
import os
from typing import Callable, Any, Optional, Tuple
from typing import List, Dict, Union
import gymnasium as gym
import time
from spider2 import configs

logger = logging.getLogger("spider2.env")
Metric = Callable[[Any, Any], float]
Getter = Callable[[gym.Env, Dict[str, Any]], Any]

class Evaluation:
    
    def _set_task_info(self, task_config: Dict[str, Any]):
        # evaluator dict
        # func -> metric function string, or list of metric function strings
        # conj -> conjunction of multiple metrics if func is a list with length > 1, "and"/"or"
        # result -> result getter config, or list of result getter configs
        # expected (optional) -> expected getter config, or list of expected getter configs
        # options (optional) -> metric options, or list of metric options
        # if func is a str list, then result, expected (if exists), options (if exists) should also be lists of the same length
        # even if one of the metrics does not need expected or options field, it should be included in the list with None
        # self.evaluator = task_config["evaluator"]
        # self.metric: Metric = [getattr(metrics, func) for func in self.evaluator["func"]] \
        # if isinstance(self.evaluator["func"], list) \
        # else getattr(metrics, self.evaluator["func"])
        # self.metric_conj: str = self.evaluator.get("conj", "and")  # take conjunction of multiple metrics
        
        
        # if "result" in self.evaluator:
        #     self.result_getter: Getter = [getattr(getters, "get_{:}".format(res["type"])) for res in
        #                               self.evaluator["result"]] \
        #     if isinstance(self.evaluator["result"], list) \
        #     else getattr(getters, "get_{:}".format(self.evaluator["result"]["type"]))
        # else:
        #     self.result_getter = [None] * len(self.metric) \
        #         if isinstance(self.metric, list) \
        #         else None

        # if "expected" in self.evaluator:
        #     self.expected_getter: Getter = [getattr(getters, "get_{:}".format(exp["type"])) if exp else None for exp in
        #                                     self.evaluator["expected"]] \
        #         if isinstance(self.evaluator["expected"], list) \
        #         else getattr(getters, "get_{:}".format(self.evaluator["expected"]["type"]))
        # else:
        #     self.expected_getter = [None] * len(self.metric) \
        #         if isinstance(self.metric, list) \
        #         else None
        # self.metric_options: Union[List[Dict[str, Any]], Dict[str, Any]] = [opt if opt else {} for opt in
        #                                                                     self.evaluator["options"]] \
        #     if isinstance(self.evaluator.get("options", {}), list) \
        #     else self.evaluator["options"] \
        #     if "options" in self.evaluator \
        #     else [{}] * len(self.metric) \
        #     if isinstance(self.metric, list) \
        #     else {}

        # assert (not isinstance(self.evaluator["func"], list)
        #         or (len(self.metric) == len(self.result_getter) == len(self.expected_getter) == len(
        #             self.metric_options)))
        
        
    # def evaluate(self):
    #     """
    #     Evaluate whether the task is successfully completed.
    #     """

    #     self.setup_controller.setup(self.evaluator.get("postconfig", []))
    #     if self.metric == "infeasible":
    #         return 0

    #     if type(self.metric) == list:
    #         results = []
    #         for idx, metric in enumerate(self.metric):
    #             try:
    #                 config = self.evaluator["result"][idx]
    #                 result_state = self.result_getter[idx](self, config)
    #                 expected = self.evaluator["expected"][idx]

    #                 expected_state = self.expected_getter[idx](self, expected) if expected else None
    #                 self.metric_options[idx]["mnt_dir"] = self.mnt_dir
    #                 self.metric_options[idx]["controller"] = self.controller
    #                 metric: int = metric(result_state, expected_state,
    #                                     **self.metric_options[idx]) if expected_state is not None \
    #                     else metric(result_state, **self.metric_options[idx])
    #             except FileNotFoundError:
    #                 logger.error("File not found!")
    #                 results.append(0.0)
    #                 continue
    #             results.append(metric)

    #         if self.metric_conj == 'and':
    #             return sum(results) / len(results)
    #         elif self.metric_conj == 'or':
    #             return max(results)
    #     else:
    #         try:
    #             result_state = self.result_getter(self, self.evaluator["result"])
    #         except FileNotFoundError:
    #             logger.error("File not found!")
    #             return 0

    #         expected_state = self.expected_getter(self, self.evaluator["expected"]) if "expected" in self.evaluator \
    #             else None

    #         metric: float = self.metric(result_state, expected_state,
    #                                     **self.metric_options) if expected_state is not None \
    #             else self.metric(result_state, **self.metric_options)

    #     return metric
    