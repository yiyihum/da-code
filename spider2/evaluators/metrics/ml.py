# import operator
from typing import Dict, List
import logging, re, os
import pandas as pd
from sklearn.metrics import f1_score, r2_score, silhouette_score
from sklearn.preprocessing import LabelEncoder
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import numpy as np


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

            unique_id_columns, target_column2 = cls.identify_columns(df, type)
            unique_column2 = unique_id_columns[0] if unique_id_columns else ""
            
            target_column = target_column2 if not target_column else target_column
            unique_column = unique_column2 if not unique_column else unique_column
        else:
            unique_id_columns, target_column = cls.identify_columns(df, type)
            for unique_column in unique_id_columns:
                if 'feature' not in unique_column.lower() or 'pca' not in unique_column.lower():
                    df.drop(unique_column, axis=1, inplace=True)
        
        return df, unique_column, target_column

    @classmethod
    def identify_columns(cls, df, type):
        target_column = None
        unique_id_columns = []
        if type == 'cluster':
            target_column = next((col for col in df.columns \
            if col.lower() in ['cluster', 'clusters']), '')

        for column in df.columns:
            if df[column].nunique() == len(df):
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
                if len(df[column].unique()) >=1 and len(df[column].unique()) < 0.5 * len(df) and df[column].dtype == 'int64':
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
    competition = config.get('competition', {'iscompetition': False})
    assert not competition['iscompetition'], f"Competition task has not been finished"

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


        

    




