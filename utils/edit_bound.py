import json
import jsonlines, os

dir_path = "evaluation_examples/examples/machinelearning"

files = os.listdir(dir_path)

evals = []
for file in files:
    file_path = os.path.join(dir_path, file)
    with open(file_path, 'r') as js:
        config = json.load(js)
    if 'binary' in file:
        config["config"]['upper_bound'] = config["config"]["threshold"]
        config["config"]['lower_bound'] = 0.5
    elif 'cluster' in file:
        config["config"]['upper_bound'] = config["config"]["threshold"]
        config["config"]['lower_bound'] = -1.0
    elif 'multi' in file:
        config["config"]['upper_bound'] = 0.90
        config["config"]['lower_bound'] = 0.2
    elif 'regression' in file:
        config["config"]['upper_bound'] = 0.90
        config["config"]["lower_bound"] = -1.0
    config["config"].pop('threshold')
    
    with open(file_path, 'w') as js:
        json.dump(config, js, indent=4)