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

experiments = [["gemini-1.5-pro-latest-ML0613", "azure-ML0608", "claude-3-opus-20240229-ML0613", "qwen-max-ML0613","llama3-70b-ML0611","mixtral-8x7b-32768-ML0613","CodeLlama-70b-Instruct-hf-ML","deepseek-coder-33b-instruct-ML","Mixtral-8x22B-Instruct-v0.1-ML"],
                ["gemini-1.5-pro-latest-visual0613", "azure-visual0614", "claude-3-opus-20240229-visual0613", "qwen-max-visual0611","llama3-70b-visual0613","mixtral-8x7b-32768-visual0611"],
                ["gemini-1.5-pro-latest-DM0613","azure-DM0612","claude-3-opus-20240229-DM0613","qwen-max-DM0613","llama3-70b-DM0613","mixtral-8x7b-32768-DM0613"],
                ["gemini-1.5-pro-latest-SA0613","azure-SA0613","claude-3-opus-20240229-SA0613","qwen-max-SA0613","llama3-70b-SA0613","mixtral-8x7b-32768-SA0613"],
                ["azure-DW0614",]]

models = ["gemini-1.5-pro-latest","gpt4-turbo","claude-3-opus-20240229","qwen-max","llama3-70b","mixtral-8x7b-32768","CodeLlama-70b-Instruct-hf","deepseek-coder-33b-instruct","Mixtral-8x22B-Instruct-v0.1"]

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


