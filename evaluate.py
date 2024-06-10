import pandas as pd
from tqdm import tqdm
from spider2.evaluators.evaluation import Evaluator
import json

def run_evaluation(output_dir, gold_dir, eval_json, result_json, timeout_seconds=10):
    # Initialize the Evaluator with the provided directories
    evaluator = Evaluator(output_dir=output_dir, gold_dir=gold_dir, timeout_second=timeout_seconds)

    # Perform the evaluation
    results_infos = evaluator.evaluate(env_config=eval_json)
    with open(result_json, 'w') as json_file:
        json.dump(results_infos, json_file, indent=4)


# Parameters
experiments = "azure-visual0605"
output_dir = f'./benchmark/output/{experiments}'
gold_dir = './benchmark/gold'
eval_json = './benchmark/configs/Evaluation_Visual.jsonl'
result_json = f'./benchmark/results/{experiments}_result.json'
timeout_seconds = 20

# Run the evaluation with the specified parameters
run_evaluation(output_dir, gold_dir, eval_json, result_json, timeout_seconds)

