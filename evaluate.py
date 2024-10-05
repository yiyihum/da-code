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
    result_type = [result['result_type'] for result in results_infos]
    types = [result['task'] for result in results_infos]
    types = ["machine learning" if "machine learning" in t else t for t in types]
    hardness = [result['hardness'] for result in results_infos]
    eda = ["data insight","data manipulation","data visualization","statistical analysis"]
    big_types = ["EDA" if t in eda else t for t in types]
    plot = ["line","pie","bar","scatter"]
    result_type = ["plot" if t in plot else t for t in result_type]
    # 统计不同类型的任务的分数，完成度
    df = pd.DataFrame({"type": types, "score": scores, "finished": finished, "hardness": hardness, "big_type": big_types,"result_type": result_type})
    print(df.groupby("type").agg({"score": "mean", "finished": "mean"}))
    print(df.groupby("hardness").agg({"score": "mean", "finished": "mean"}))
    print(df.groupby("big_type").agg({"score": "mean", "finished": "mean"}))
    print(df.groupby("result_type").agg({"score": "mean", "finished": "mean"}))
    average_score = sum(scores) / num_results
    average_finished = sum(finished) / num_results
    results_json = {"num_results": num_results, "average_score": average_score, "results": results_infos, "average_finished": average_finished}
    print(f"Number of results: {num_results}")
    print(f"Average score: {average_score}")
    print(f"Average finished: {average_finished}")

    
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
