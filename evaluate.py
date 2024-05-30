import argparse
from tqdm import tqdm
from spider2.evaluators.evaluation import Evaluator

output_dir = './benchmark/results/azure-DV-test'
gold_dir = './benchmark/gold'

evalutor = Evaluator(output_dir=output_dir, gold_dir=gold_dir)

eval_json = 'benchmark/configs/evaluation000.json'

score, info = evalutor.evaluate(env_config=eval_json)
print(score) # 1.0
if info:
    print(info)
'''
[{'img': False, 'data': True, 'type': True, 'color': True, 'figsize': True, 'labels': True, 'xtick_labels': True, 'ytick_labels': True}]
'''
