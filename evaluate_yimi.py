import pandas as pd
from tqdm import tqdm
from spider2.evaluators.evaluation import Evaluator
import json
import os

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

timeout_seconds = 60


models = ["gemini-1.5-pro-latest","gpt4-turbo","claude-3-opus-20240229","qwen-max","llama3-70b","mixtral-8x7b-32768","CodeLlama-70b-Instruct-hf","CodeLlama-34b-Instruct-hf","deepseek-coder-33b-instruct","Mixtral-8x22B-Instruct-v0.1","gpt-4o","gpt-3.5-turbo","Qwen2-72B-Instruct"]
models = ["Qwen2-72B-Instruct"]

for model in models:
    eval_json=f'benchmark/configs/Evaluation_EDA_ML.jsonl'
    output_dir = f'./benchmark/output/{model}'
    gold_dir = './benchmark/gold'
    output_file = f'./benchmark/results/{model}_result.json'
    if not os.path.exists(output_dir):
        print(f"Output directory {output_dir} does not exist. Skipping evaluation.")
        continue
    # if os.path.exists(output_file):
    #     print(f"Results file {output_file} already exists. Skipping evaluation.")
    #     continue

    print(f"Evaluating {model}...")
    run_evaluation(output_dir, gold_dir, eval_json, output_file, timeout_seconds)
    print(f"Results saved to {output_file}")
    print()
    print()


