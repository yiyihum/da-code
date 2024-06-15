import jsonlines, json, os


ins_path = 'benchmark/configs/ML.jsonl'
eval_path = 'benchmark/configs/Evaluation_ML_wo_thr.jsonl'


with jsonlines.open(ins_path, 'r') as f:
    ins = [line for line in f]
    
with jsonlines.open(eval_path, 'r') as f:
    evals = [line for line in f]
    
levels = {}

for fig in ins:
    id = fig["id"]
    level = fig["hardness"]
    levels[id] = level

evals2 = []
for eval in evals:
    id = eval["id"]
    if id not in levels.keys():
        continue
    eval["config"]["hardness"] = levels[id]
    evals2.append(eval)

eval_path = 'benchmark/configs/Evaluation_ML_wo_thr2.jsonl'
with jsonlines.open(eval_path, 'w') as js:
    js.write_all(evals2)


    