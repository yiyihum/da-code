# import operator
from typing import List
import logging, re, os
import pandas as pd
from sklearn.metrics import f1_score, r2_score, silhouette_score
from sklearn.preprocessing import LabelEncoder
from fuzzywuzzy import process
import numpy as np
import difflib
from sklearn.metrics import roc_auc_score

TYPES = ['binary classification', 'multi classification', 'cluster', 'regression']

METRICS = {
    "binary": 'f1', 
    "multi": 'f1', 
    "regression": "r2",
    "cluster": 'silhouette score'
}

class PreprocessML:
    
    @staticmethod
    def check_numeric_columns(df):
        """
        Check if all elements in all columns of the DataFrame are numerical.
        """
        non_numeric_columns = []
        for column in df.columns:
            try:
                pd.to_numeric(df[column])
            except ValueError:
                non_numeric_columns.append(column)
        return non_numeric_columns

    @classmethod
    def process_csv(cls, df: pd.DataFrame, type, **kwargs):
        if type != 'cluster':
            unique_column = kwargs.get('unique_column', '')
            target_column = kwargs.get('target_column', '')
            columns = list(df.columns)
            if unique_column:
                best_unique_column, ratio = process.extractOne(unique_column, columns)
                if ratio > 90:
                    unique_column = best_unique_column
                    df = df.sort_values(by=unique_column)
                else:
                    unique_column = ''
            if target_column:
                best_target_column, ratio = process.extractOne(target_column, columns)
                target_column = best_target_column if ratio > 90 else ''

            if target_column and unique_column:
                return df, unique_column, target_column

            unique_id_columns, target_column2 = cls.identify_columns(df, type, target_column)
            unique_column2 = unique_id_columns[0] if unique_id_columns else ""   
            target_column = target_column2 if not target_column else target_column
            unique_column = unique_column2 if not unique_column else unique_column
            if unique_column:
                df = df.sort_values(by=unique_column)
        else:
            unique_id_columns, target_column = cls.identify_columns(df, type)
            for unique_column in unique_id_columns:
                if 'feature' not in unique_column.lower() or 'pca' not in unique_column.lower():
                    df.drop(unique_column, axis=1, inplace=True)
        
        return df, unique_column, target_column

    @classmethod
    def identify_columns(cls, df, type, ref_column: str=None):
        target_column = None
        columns = list(df.columns)
        ref_column = ref_column if type != 'cluster' else 'Cluster'
        if ref_column:
            columns = sorted(columns, key=lambda x: difflib.SequenceMatcher(None, x.lower(), ref_column.lower()).ratio(), reverse=True)
            columns = [item for item in columns if difflib.SequenceMatcher(None, item.lower(), ref_column.lower()).ratio() >= 0.5]
        unique_id_columns = []
        for column in columns:
            if ('id' in column.lower() or 'unnamed' in column.lower()) and df[column].nunique() == len(df):
                unique_id_columns.append(column)
            if type =='binary':
                if len(df[column].unique()) == 2: 
                    target_column = column if not target_column \
                        else target_column
            elif type == 'multi':
                if len(df[column].unique()) > 2 and len(df[column].unique()) < 10:
                    target_column = column if not target_column \
                        else target_column
            elif type == 'cluster':
                if len(df[column].unique()) >=1 and len(df[column].unique()) < 0.6 * len(df):
                    target_column= column if not target_column else target_column
        return unique_id_columns, target_column

class CalculateML:

    @staticmethod
    def calculate_r2(gold, result):
        output = {'errors':[]}
        if not str(gold.dtype) == str(result.dtype) :
            try:
                result.astype(str(gold.dtype))
            except TypeError as e:
                output['errors'].append(f"TypeError: result target dtype {str(result.dtype)} is not compatible with gold's {str(gold.dtype)}. Error: {str(e)}")
                return (0.0, output)
            except ValueError as e:
                output['errors'].append(f"ValueError: result target dtype {str(result.dtype)} cannot be converted to gold's {str(gold.dtype)}. Error: {str(e)}")
                return (0.0, output)
            except Exception as e:
                output['errors'].append(f"Unexpected error: {str(e)}")
                return (0.0, output)
            output['errors'].append(f"TypeError: result target dtype {str(result.dtype)} is not compatible with gold's {str(gold.dtype)}.")
        try:
            score = r2_score(y_true=gold, y_pred=result)
        except Exception as e:
            output['errors'].append(f'fall to calculate r2 socre, because {str(e)}')
            return (0.0, output['errors'])
        
        return (max(score, 0.0), output)
    
    @staticmethod
    def calculate_f1(gold, result):
        output = {'errors': []}
        if not str(gold.dtype) == str(result.dtype):
            output['errors'].append(f"TypeError: result target dtype {str(result.dtype)} is not compatible with gold's {str(gold.dtype)}.")
        label_encoder = LabelEncoder()
        gold = label_encoder.fit_transform(gold)
        result = label_encoder.fit_transform(result)
        try:
            score = f1_score(y_true=gold, y_pred=result, average='weighted')
        except Exception as e:
            output['errors'].append(f'fall to calculate f1 socre, because {str(e)}')
            return (0.0, output['errors'])

        return (score, output)
    
    @staticmethod
    def calculate_silhouette(result,target_labels):
        target_labels = target_labels if isinstance(target_labels, np.ndarray) \
            else np.array(target_labels)
        output = {'errors': []}
        non_numeric_columns = PreprocessML.check_numeric_columns(result)
        if len(non_numeric_columns) > 0:
            output['errors'].append(f'result contains non numeric columns: {list(non_numeric_columns)}')
            for col in non_numeric_columns:
                try:
                
                    le = LabelEncoder()
                    result[col] = le.fit_transform(result[col])
                except Exception as e:
                    output['errors'].append(f'Column "{col}" contains non-numeric values that cannot be converted')
                    return (0.0, output)
        
        if len(np.unique(target_labels)) == 1:
            output['errors'].append(f'"target labels only contain 1 clusters, which must needs 2 or more clusters')
            return (0.0, output)
        
        try:
            score = silhouette_score(result, target_labels)
        except Exception as e:
            output['errors'].apppend(f"fail to calculate silhouette_score: {str(e)}")
        return (score, output)
    
    @staticmethod
    def calculate_roc_score(result: pd.DataFrame, gold: pd.DataFrame, task_type: str):
        output = {'errors': []}
        try:
            result_np = result.to_numpy()
        except Exception as e:
            output['errors'].append(f'result csv fails to be converted to numpy, because {str(e)}')
            return (0.0, output)
        gold_np = gold.to_numpy()
        if task_type == 'binary':
            result_np = result_np[:, 1]
            if gold_np.ndim == 2:
                gold_np = gold_np[:, 1]
            try:
                score = roc_auc_score(y_true=gold_np, y_score=result_np)
            except Exception as e:
                output['errors'].append(f'fails to calculate roc_auc_score, because {str(e)}')
                return (0.0, output)
            return score, output
        elif task_type == 'multi':
            if result_np.ndim != 2:
                raise ValueError("The result array should be a 2D array.")
            elif result_np.shape[-1] < 3:
                raise ValueError('The result csv should contains 3 more columns')
            row_sum = np.sum(result_np, axis=1)
            if not np.allclose(row_sum, 1):
                raise ValueError("At least one row has probabilities that don't sum to 1.")
            try:
                score = roc_auc_score(y_true=gold_np, y_score=result_np)
            except Exception as e:
                output['errors'].append(f'fails to calculate roc_auc_score, because {str(e)}')
                return (0.0, output)
            return score, output
    
    def calculate_logloss(result:pd.DataFrame, gold: pd.DataFrame, task_type: str):
        output = {'errors': []}
        try:
            result_np = result.to_numpy()
        except Exception as e:
            output['errors'].append(f'result csv fails to be converted to numpy, because {str(e)}')
            return (0.0, output)
        gold_np = gold.to_numpy()
        result_np = result_np / result_np.sum(axis=1, keepdims=True)
        pass

        
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
    output_ml = {'errors': []}
    config = kwargs.get('config', {})
    target_column = kwargs.get('target_column', '')
    assert config, 'Machine Learning Evaluation needs a config.'
    task_type = config.get('type', '')
    assert task_type, f'Machine Learning Evaluation needs "type" in config, such as {TYPES}'

    metric = config.get("metric", "")
    threshold = config.get("threshold", 0.9)

    best_type, ratio = process.extractOne(task_type, TYPES)
    assert ratio > 90, f"please provide a right task type, such as {TYPES}"
    task_type = best_type.split(' ')[0]
    if not metric:
        metric = METRICS[task_type]
    output_ml.update({'metric': metric})
    output_ml.update({'threshold': threshold})

    gold = ''
    if task_type != 'cluster':
        expected = expected if isinstance(expected, list) else [expected]
        gold = next((file for file in expected if file.endswith('.csv')), '')
        assert os.path.exists(gold), f'gold file path {gold} does not exist'
    result = result if isinstance(result, list) else [result]
    result = next((file for file in result if file.endswith('.csv')), '')
    assert result or gold, f'Machine Learning Evaluation can only evaluate csv file, please check again'
    if not os.path.exists(result):
        output_ml['errors'].append(f'result file {result} does not exists')
        output_ml['score'] = 0.0
        return output_ml

    if task_type != 'cluster':
        gold_df = pd.read_csv(gold)
        result_df = pd.read_csv(result)

        if not len(gold_df) == len(result_df):
            output_ml['errors'].append(f'The length of the result content is not equal to the length of the true value.')
            output_ml['score'] = 0.0
            return output_ml
        
        if not len(gold_df.columns) == len(result_df.columns):
            output_ml['errors'].append(f"result csv columns are different from gold csv: {list(set(result_df.columns) - set(gold_df.columns))}")
    
        gold_df, unique_column_gold, target_column_gold \
            = PreprocessML.process_csv(gold_df, task_type, **{'target_column': target_column})
        column_dict = {'unique_column': unique_column_gold,
                'target_column': target_column_gold}
        
        result_df, _, target_column_result \
            = PreprocessML.process_csv(result_df, task_type, **column_dict)
        
        if not target_column_result:
            output_ml['errors'].append(f'Could not find target column in result, which is {target_column_gold} in gold')
            output_ml['score'] = 0.0
            return (0.0, output_ml)

        output_ml['target_output'] = target_column_result

        if not target_column_result:
            output_ml['errors'].append(f'Could not find target column in result, gold target column is {target_column_gold}, and provided result column is {result_df.columns}')
            output_ml['score'] = 0.0
            return output_ml
        metric_func = getattr(CalculateML, f'calculate_{metric}')
        if not metric_func:
            raise ValueError(f'Now do not support func calculate_{metric}')
        target_gold = gold_df[target_column_gold]
        target_result = result_df[target_column_result]
        score, output = metric_func(target_gold, target_result)
        output_ml['errors'].extend(output['errors'])
        output_ml['score'] = score
        return output_ml
    else:
        result_df = pd.read_csv(result)
        result_df, _, target_column_result \
            = PreprocessML.process_csv(result_df, task_type)
        if not target_column_result:
            output_ml['errors'].append(f'Could not find target column in result, and provided result column is {list(result_df.columns)}')
            output_ml['score'] = 0.0
            return output_ml
        target_labels = result_df[target_column_result].tolist()
        if not metric == 'silhouette score':
            logging.error('Cluster task only support silhouette score to evaluate')
        score, output = CalculateML.calculate_silhouette(result=result_df, target_labels=target_labels)
        output_ml['errors'].extend(output['errors'])
        output_ml['score'] = score
        return output_ml

def compare_competition_ml(result: str, expected: str|List[str], **kwargs) -> dict:
    output_ml = {'errors': []}
    config = kwargs.get('config', {})
    assert config, 'Machine Learning Evaluation needs a config.'
    task_type = config.get('type', '')
    assert task_type, f'Machine Learning Evaluation needs "type" in config, such as {TYPES}'
    metric = config.get("metric", "")

    best_type, ratio = process.extractOne(task_type, TYPES)
    assert ratio > 90, f"please provide a right task type, such as {TYPES}"
    task_type = best_type.split(' ')[0]
    if not metric:
        metric = METRICS[task_type]
    
    expected = expected if isinstance(expected, list) else [expected]
    result = result if isinstance(result, list) else [result]
    assert len(result) == 1, "Just need one result csv file"
    leaderboard = [file for file in expected if 'leaderboard' in os.path.basename(file).lower()]
    if len(leaderboard) != 1:
        raise ValueError('Please provide one "leaderboard.csv"')
    leaderboard = leaderboard[0]
    expected = [file for file in expected if os.path.basename(file) == os.path.basename(result)]
    if len(expected) != 1:
        raise ValueError(f"Can't find gold csv file {os.path.basename(result)}")
    expected = expected[0]

    if not os.path.exists(expected):
        raise FileNotFoundError(f"The gold file '{os.path.basename(expected)}' does not exist.")
    if not os.path.exists(leaderboard):
        raise FileNotFoundError(f"The leaderboard file '{os.path.basename(leaderboard)}' does not exist.")
    if not os.path.exists(result):
        output_ml['errors'].append(f'result file {os.path.basename(result)} does not exist')
        output_ml['score'] = 0.0
        return output_ml
    
    expected_df = pd.read_csv(expected)
    result_df = pd.read_csv(result)
    expected_columns = list(expected_df.columns)
    result_columns = list(result_df.columns)

    if len(result_df) != len(expected_df):
        output_ml['errors'].append(f"Length mismatch: result CSV has {len(result_df)} rows, while expected CSV has {len(expected_df)} rows.")
        output_ml['score'] = 0.0
        return output_ml
    if set(result_columns) != set(expected_columns):
        output_ml['errors'].append(f'Unexpected Column: {list(set(result_df.columns) - set(expected_df.columns))}')
        output_ml['score'] = 0.0
        return output_ml
    
    id = next((col for col in expected_columns if 'id' in col.lower()), '')
    if id:
        expected_df = expected_df.sort_values(by=id)
        result_df = result_df.sort_values(by=id)
        expected_df.drop(id, inplace=True, axis=1)
        result_df.drop(id, inplace=True, axis=1)
    
    expected_df.sort_index(axis=1, inplace=True)
    result_df.sort_index(axis=1, inplace=True)

    # metric_func =




    

    

    
    


