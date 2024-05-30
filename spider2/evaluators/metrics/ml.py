# import operator
from typing import Dict, List, Tuple
from dataclasses import dataclass
import logging, yaml, re
import pandas as pd
from sklearn.metrics import f1_score
from sklearn.preprocessing import LabelEncoder


@dataclass
class CalculateML:
    container_name : str= "spider2"

    @staticmethod
    def read_csv(filename):
        df = pd.read_csv(filename)
        if len(df) == 0:
            result = []
        elif len(df) == 1:
            result = df.iloc[:, 0].tolist()
        elif len(df) == 2:
            if "Unnamed: 0" in df.columns:
                df = df.drop("Unnamed: 0", axis=1)
            if "Unnamed:0" in df.columns:
                df = df.drop("Unnamed:0", axis=1)
            if len(df) == 1:
                result = df.iloc[:, 0].tolist()
            else:
                result = []
        else:
            label = ""
            for hyp_label in LABELS:
                for ref_label in df.columns:
                    if hyp_label == ref_label:
                        label = hyp_label
                        break
            result = df[label].tolist() if label else []
        return result
   
    @staticmethod
    def calculate_labels(hyp_label, ref_label, threshold=0.9):
        labels = set(hyp_label)
        if len(labels) <=2:
            score = f1_score(ref_label, hyp_label)
        else:
            score = f1_score(ref_label, hyp_label, average="micro")
        if score >= threshold:
            return 1.0
        else:
            return score / threshold
        
        
def compare_ml(result: str, expected: str|List[str], **kwargs) -> dict:
    """ 
    @args:
        result(str): the pred text file
        expect(str|List[str]): the gold output file
        option(dict): the configuration dictionary
    @return:
        the dict contains of results of metrics
        # filepath: the filepath containing target db content if found, otherwise None
    """
    mnt_dir = options.pop('mnt_dir')
    controller = options.pop('controller')
    expected = expected if isinstance(expected, list) else [expected]
    yaml_file = [file for file in expected if file.endswith('.yaml')]
    try:
        yaml_path = yaml_file[0]
        with open(yaml_path, 'r') as file:
            data = yaml.safe_load(file)
    except:
        data = {"time": 60, "metric": 0.9}
    
    def parse_result(file: str):
        suffix = file[-3:]
        parse_func = f'read_{suffix}'
        if not hasattr(CalculateML, parse_func):
            raise NotImplementedError(f'FileType {suffix} is not implemented')
        return getattr(CalculateML, parse_func)(file)
    
    hyp_result = parse_result(result)
    if not hyp_result:
        return 0.0
    
    ref_results = [parse_result(file) for file in expected if file.endswith((".txt", ".csv"))]
    assert len(ref_results) > 0, "Please provide gold results in type of ['.txt' ,'.csv']"
    ref_result = ref_results[0]
    label_encoder = LabelEncoder()
    hyp_result = label_encoder.fit_transform(hyp_result)
    ref_result = label_encoder.fit_transform(ref_result)
    
    score1 = CalculateML.calculate_labels(hyp_label=hyp_result, ref_label=ref_result, threshold=data.get("metric", 0.9))
    if not os.path.exists(mnt_dir):
        return score1
    
    sk_files = CalculateML.find_py(mnt_dir=mnt_dir)
    if not sk_files:
        return score1
    score2s = [CalculateML.evaluate_time(sk_file, mnt_dir, controller, data.get("time", 30)) for sk_file in sk_files]
    score2 = min(score2s)

    return (score1 + score2) / 2




