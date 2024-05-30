# import operator
from typing import Dict, List, Tuple
from dataclasses import dataclass
import logging, yaml, re
import pandas as pd
from sklearn.metrics import f1_score
from sklearn.preprocessing import LabelEncoder
import sys, threading, os
from pathlib import Path
here = Path(__file__).absolute().parent.parent
sys.path.append(str(here.parent))
from controllers.python import PythonController
# from envs.spider2 import DEFAULT_WORK_DIR

DEFAULT_WORK_DIR = '/workspace'
LABELS = ['label', 'labels', 'output','result', 'results', 'Label', 'Labels', 'Output',"Result","Results"]

def run_command(container, cmd, result_holder, work_dir=DEFAULT_WORK_DIR):
    result = container.exec_run(cmd, workdir=work_dir)
    result_holder.append(result)

def exec_with_timeout(container, cmd, timeout, work_dir):
    result_holder = []
    thread = threading.Thread(target=run_command, args=(container, cmd, result_holder, work_dir))
    thread.start()
    thread.join(timeout)
    if thread.is_alive():
        print("Command timed out")
        return None
    return result_holder[0]


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
    def read_txt(filename):
        try:
            with open(filename, 'r') as f:
                result = f.readlines()
        except:
            result = []
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
        
    @staticmethod
    def find_py(mnt_dir):
        py_files = [os.path.join(mnt_dir, py_path) for py_path in os.listdir(mnt_dir) \
            if os.path.isfile(os.path.join(mnt_dir, py_path)) and py_path.endswith('.py')]
        assert len(py_files) > 0, f"{mnt_dir} contains no py files"
        '''
        Find the py file used to generate the result image
        '''
        def is_sklearn(filename: str):
            with open(filename, 'r') as f:
                file_content = f.readlines()
            stores = ['sklearn', 'xgboost']
            _find = False
            for line in file_content:
                for store in stores:
                    if store in line:
                        _find = True
                        break
            return _find
    
        plt_files = [py_path for py_path in py_files if is_sklearn(py_path)]
        return plt_files

    @classmethod
    def evaluate_time(cls, py_file: str, mnt_dir: str, controller: PythonController, threshold: float=60):
        py_file = py_file.replace(mnt_dir, DEFAULT_WORK_DIR) 
        cmd = f'bash -c "time python {py_file}"'
        outputs = exec_with_timeout(container=controller.container, cmd=cmd, timeout=2 * threshold, work_dir=DEFAULT_WORK_DIR)
        output = outputs.output.decode('utf-8')
        use_time = cls.extract_real_time(output)
        if use_time:
            if use_time < threshold:
                return 1.0
            else:
                return (2*threshold - use_time) / threshold
        else:
            return 0.0 

    @staticmethod
    def extract_real_time(log_string):
        pattern = r"real\s+(\d+m\d+\.\d+s)"
        match = re.search(pattern, log_string)
        if match:
            time_string =  match.group(1)
        else:
            return 0
        minutes, seconds = map(float, re.findall(r'\d+\.\d+|\d+', time_string))
        return minutes * 60 + seconds
        

def compare_ml(result: str, expected: str|List[str], **options) -> dict:
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




