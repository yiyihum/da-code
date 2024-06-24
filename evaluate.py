import pandas as pd
from tqdm import tqdm
from da_agent.evaluators.evaluation import Evaluator
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
experiment = 'gpt-4'
output_dir = f'./da_code/output/{experiment}'
gold_dir = './da_code/gold'
eval_json = './da_code/configs/eval_example.jsonl'
output_file = f'./da_code/results/{experiment}_results.json'
timeout_seconds = 60

# Run the evaluation with the specified parameters
run_evaluation(output_dir, gold_dir, eval_json, output_file, timeout_seconds)

