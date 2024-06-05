import json
import jsonlines, os

dir_path = 'evaluation_examples/examples/datavisualization'
files = [os.path.join(dir_path, file) for file in os.listdir(dir_path)]
files = sorted(files)
evals = []
for file in files:
    with open(file, 'r') as f:
        eval_dict = json.load(f)
    evals.append(eval_dict)

with jsonlines.open('evaluation_examples/examples/machinelearning/Evaluation_Visual.jsonl', 'w') as f:
    for item in evals:
        f.write(item)