import argparse
import pandas as pd
from tqdm import tqdm
from da_agent.evaluators.evaluation import Evaluator
import json
import os

def run_evaluation(output_dir, gold_dir, eval_json, output_file, timeout_seconds):
    # Initialize the Evaluator with the provided directories
    evaluator = Evaluator(output_dir=output_dir, gold_dir=gold_dir, timeout_seconds=timeout_seconds)

    # Perform the evaluation
    results_infos = evaluator.evaluate(env_config=eval_json)
    num_results = len(results_infos)
    scores = [result['total_score'] for result in results_infos]
    finished = [result['finished'] for result in results_infos]
    types = [result['task'] for result in results_infos]
    types = ["machine learning" if "machine learning" in t else t for t in types]
    # 统计不同类型的任务的分数，完成度
    df = pd.DataFrame({"type": types, "score": scores, "finished": finished})
    print(df.groupby("type").agg({"score": "mean", "finished": "mean"}))
    average_score = sum(scores) / num_results
    results_json = {"num_results": num_results, "average_score": average_score, "results": results_infos}
    print(f"Number of results: {num_results}")
    print(f"Average score: {average_score}")

    
    # Ensure the directory exists before writing to the file
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, 'w') as json_file:
        json.dump(results_json, json_file, indent=4)

def parse_arguments():
    parser = argparse.ArgumentParser(description="Run evaluations for NLP models.")
    parser.add_argument("--output_dir", type=str, required=True, help="Directory for output files")
    parser.add_argument("--gold_dir", type=str, default="da_code/gold", help="Directory containing gold standard files")
    parser.add_argument("--eval_json", type=str, required=True, help="JSON file with evaluation configurations")
    parser.add_argument("--result_file", type=str, required=True, help="File to write evaluation results to")
    parser.add_argument("--timeout_seconds", type=int, default=300, help="Timeout for each evaluation in seconds")
    return parser.parse_args()

def main():
    args = parse_arguments()
    run_evaluation(args.output_dir, args.gold_dir, args.eval_json, args.result_file, args.timeout_seconds)

if __name__ == "__main__":
    main()
