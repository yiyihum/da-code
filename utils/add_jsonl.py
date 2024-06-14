import jsonlines, json


LOWER_METRICS = ["logloss_class", "logloss_total", "rmsle", "mae", "mse", "smape", "medae", "crps"]
with jsonlines.open('./benchmark/configs/Evaluation_ML.jsonl', 'r') as js:
    lines = [line for line in js]

configs = []    
for line in lines:
    id = line['id']
    if 'regression' in id or 'multi' in 'id':
        configs.append(line)
        continue
    metric = line['config']['metric']
    if metric in LOWER_METRICS:
        line['config']['upper_bound'] = line['config']['upper_bound'] * 0.9
    else:
        line['config']['upper_bound'] = line['config']['upper_bound'] / 0.9

    
    if "competition" in id:
        if metric in LOWER_METRICS:
            line['config']['lower_bound'] = line['config']['lower_bound'] * 0.9
        else:
            line['config']['lower_bound'] = line['config']['lower_bound'] / 0.9
            
    configs.append(line)

with jsonlines.open('./benchmark/configs/Evaluation_ML2.jsonl', 'w') as js:
    js.write_all(configs)
        
    

