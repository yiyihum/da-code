import pandas as pd
from tqdm import tqdm
from spider2.evaluators.evaluation import Evaluator
import json

def run_evaluation(output_dir, gold_dir, eval_json, output_file, timeout_seconds=10):
    # Initialize the Evaluator with the provided directories
    evaluator = Evaluator(output_dir=output_dir, gold_dir=gold_dir, timeout_second=timeout_seconds)

    # Perform the evaluation
    results_infos = evaluator.evaluate(env_config=eval_json)
    num_results = len(results_infos)
    scores = [result['total_score'] for result in results_infos]
    average_score = sum(scores) / num_results
    results_json = {"num_results": num_results, "average_score": average_score, "results": results_infos}
    print(f"Number of results: {num_results}")
    print(f"Average score: {average_score}")
    with open(output_file, 'w') as json_file:
        json.dump(results_json, json_file, indent=4)

# Parameters
experiments = "azure-ML0611"
output_dir = f'./benchmark/_result/azure-ML0611'
gold_dir = './benchmark/gold'
eval_json = './benchmark/configs/Evaluation_ML2.jsonl'
output_file = f'./benchmark/results/{experiments}_result22.json'
timeout_seconds = 6000

# Run the evaluation with the specified parameters
run_evaluation(output_dir, gold_dir, eval_json, output_file, timeout_seconds)

