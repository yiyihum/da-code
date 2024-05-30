# import operator
from typing import Dict, List, Tuple
from rouge import Rouge
import numpy as np
from typing import Dict, List, Set
from typing import List
import nltk
from nltk import edit_distance
from dataclasses import dataclass
import logging

METRICS = ['bleu', 'rouge', 'meteor', 'edit distance']
def exist_metrics(metric):
    similarity_metric = [edit_distance(metric, gold_metric) for gold_metric in METRICS]
    max_value = min(similarity_metric)
    max_index = similarity_metric.index(max_value)
    return METRICS[max_index]

@dataclass
class CalculateText:
    @staticmethod
    def calculate_bleu(hyp_text: str, ref_text: List[str]):
        metrics = {'bleu': np.nan}
        hyp_text = hyp_text.split()
        ref_text = [ref.split() for ref in ref_text]
        metrics["bleu"] = nltk.translate.bleu(ref_text, hyp_text)
        return metrics
    
    @staticmethod
    def calculate_edit_distance(hyp_text: str, ref_text: List[str]):
        metrics = {'edit distance': np.nan}
        edit_distance_metrics = [edit_distance(hyp_text, gt) \
                / max(len(gt), len(hyp_text)) for gt in ref_text]
        if len(edit_distance_metrics) > 0:
            metrics["edit distance"] = sum(edit_distance_metrics) / len(edit_distance_metrics)
        else:
            metrics["edit distance"] = np.nan
        return metrics
    
    @staticmethod
    def calculate_meteor(hyp_text: str, ref_text: List[str]):
        metrics = {'meteor': np.nan}
        hyp_text = hyp_text.split()
        ref_text = [ref.split() for ref in ref_text]
        try:
            metrics['meteor']  = nltk.translate.meteor(ref_text, hyp_text)
        except LookupError:
            metrics['meteor'] = np.nan
        
        return metrics
   
    @staticmethod
    def calculate_rouge(hyp_text: str, ref_text: List[str]):
        metrics = {"rouge-1": np.nan,
            "rouge-2": np.nan,
            "rouge-l": np.nan}
        rouge = Rouge()
        scores = rouge.get_scores([hyp_text], ref_text, avg=True)
        metrics["rouge-1"] = scores["rouge-1"]["f"]
        metrics["rouge-2"] = scores["rouge-2"]["f"]
        metrics["rouge-l"] = scores["rouge-l"]["f"]
        return metrics
    
def compare_text(result: str, expected: str|List[str], metrics: str|List[str], minlen: int=4, **options) -> dict:
    """ 
    @args:
        result(str): the pred text file
        expect(str|List[str]): the gold text file or text files, maybe multiple potential answers, not there are two answers
        option(dict): the configuration dictionary
    @return:
        the dict contains of results of metrics
        # filepath: the filepath containing target db content if found, otherwise None
    """
    metrics_results = {}
    metrics = metrics if isinstance(metrics, list) else [metrics]
    if isinstance(expected, list):
        '''
        condition_cols = options.get('condition_cols', [[]]*len(expected))
        score_rule = options.get('score_rule', ['all']*len(expected))
        ignore_order = options.get('ignore_order', [False]*len(expected))
        total_scores = options.get('total_scores', [1]*len(expected))
        '''
    elif isinstance(expected, str):
        '''
        condition_cols = [options.get('condition_cols', [])]
        score_rule = [options.get('score_rule', 'all')]
        ignore_order = [options.get('ignore_order', False)]
        total_scores = [options.get('total_scores', 1)]
        '''
        expected = [expected]

    try:
        with open(result, 'r') as r:
            hyp_result = r.read()
        ref_results = []
        for ref in expected:
            with open(ref, 'r') as r:
                ref_results.append(r.read())
    except FileNotFoundError:
        raise "Please check path of files you provid"
    
    # still to implement the Fact Query function
    if not "..." in metrics and len(hyp_result) < minlen:
        return metrics_results

    # function to calculate metrics
    def calculate_metric(metric: str, hyp_text: str, ref_text: List[str]):
        metric = metric.replace(' ', '_')
        metric_func = f'calculate_{metric.lower()}'
        if not hasattr(CalculateText, metric_func):
            raise NotImplementedError(f'Metric {metric} is not implemented, Do you mean {exist_metrics(metric.lower())}?')
        return getattr(CalculateText, metric_func)(hyp_text, ref_text)

    # Calulate metrics
    for metric in metrics:
        output = calculate_metric(metric, hyp_text=hyp_result, ref_text=ref_results)
        metrics_results.update(output)
    
    return metrics_results

if __name__ == '__main__':
    hyp_test = '/Users/stewiepeter/Desktop/VsProjects/VaftBench/text_test/hyp.txt'
    ref_test = '/Users/stewiepeter/Desktop/VsProjects/VaftBench/text_test/ref.txt'
    print(compare_text(hyp_test, [ref_test], metrics=METRICS))

