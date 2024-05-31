import pandas as pd
from tqdm import tqdm
from spider2.evaluators.evaluation import Evaluator

output_dir = './benchmark/output/example'
gold_dir = './benchmark/gold'

evalutor = Evaluator(output_dir=output_dir, gold_dir=gold_dir)

eval_json = './evaluation_examples/examples/machinelearning/ml-cluster-001.json'

score, info = evalutor.evaluate(env_config=eval_json)
print(score) # 1.0
if info:
    print(info)
'''
[{'errors': ["result contains non numeric columns: ['Genre']"], 
'metric': 'silhouette score', 
'threshold': 0.5, 
'score': 0.44637121804301805, 
'task': 'machinelearning', 
'type': 'cluster', 
'competition': {'iscompetition': False}, 
'file': 'cluster.csv', 'id': 'ml-cluster-001'}]
'''
