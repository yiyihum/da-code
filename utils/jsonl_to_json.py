import jsonlines, json, os

with jsonlines.open("/Users/stewiepeter/Desktop/VsProjects/VaftBench/dabench/benchmark/configs/evaluation_ML.jsonl", 'r') as f:
    lines = [line for line in f]


dir_path = 'evaluation_examples/examples/machinelearning'

for line in lines:
    id = line['id']
    id_path = os.path.join(dir_path, id + '.json')
    if os.path.exists(id_path):
        continue
    with open(id_path, 'w') as js:  
        json.dump(line, js, indent=4)