import pandas as pd
import jsonlines
import openai,re, os, json
from openai import OpenAI
from tqdm import tqdm
client = OpenAI(
    # This is the default and can be omitted
    api_key=os.environ.get("OPENAI_API_KEY"),
)


model = 'gpt-4'
system_message = """
You are a prompt engineer tasked with helping users extract the output file name from the prompt.

# Objective # 
Identify the output file name mentioned in the user's prompt.

# Response Format #
1. Respond with the target file name enclosed in quotation marks, such as "result.csv".
2. If the target file name is not found, respond with Not Found

# Example #
[input]
This is a dataset for the Predict Health Outcomes of Horses competition, with relevant descriptions provided in the README.md file. As a participant, you need to complete the competition requirements by predicting the results for test.csv and writing them into submission.csv following the format of sample_submission.csv.
[response]
"submission.csv"
[input]
This is a Diabetes Prediction dataset, with relevant descriptions provided in the README.md file. Based on the body information in test.csv, you need to predict whether they have diabetes.
[response]
Not Found
[input]
This is a Stroke Prediction dataset, with relevant descriptions provided in the README.md file. Based on the information in test.csv, you need to predict whether the individuals will have a stroke and write the predicted results into a file named stroke.csv, with the column name "stroke."
[response]
"stroke.csv"

Now, Let's start.
"""


jsonl_path = './benchmark/configs/ML.jsonl'
json_l= []


with jsonlines.open(jsonl_path) as reader:
    json_l = [config_json for config_json in reader]

eval_config = {
        "task": "machinelearning competition",
        "type": "",
        "metric": "",
        "threshold": 0.0
    }

eval_l = []
failed_id = []
eval_configs = []
for config in tqdm(json_l):
    id = config['id']
    messages = []
    messages.append({'role': 'system', "content": system_message})
    instruction = config['instruction']
    messages.append({"role": 'user','content': f'\n[input]\n{instruction}'})
    try:
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=0.0, # this is the degree of randomness of the model's output
        )
        response  = response.choices[0].message.content
    except Exception as e:
        print(e)
        failed_id.append(id)
        continue
    file = ''
    if "not found" in response.lower() or "notfound" in response.lower():
        raise ValueError(f'Not Found Output: {instruction}')
    else:
        matches = [match for match in re.findall(r'"([^"]*)"', str(response))]
        if len(matches) != 1:
            failed_id.append(id)
            continue
        else:
            file = matches[0]
    if not file:
        failed_id.append(id)
        continue

    eval_config = {
        "id": "",
        "config": dict({
            "task": "machinelearning",
            "type": "",
            "metric": "",
            "threshold": 0.0
        }),
        "func":[
            "compare_ml"
        ],
        "result":[
            dict({
                "file": ""
            })
        ],
        "options": [{}]
    }
    if 'binary' in id:
        eval_config["config"]["type"] = 'binary classification'
        eval_config["config"]['metric'] = 'f1'
    elif 'multi' in id:
        eval_config["config"]["type"] = 'multi classification'
        eval_config["config"]['metric'] = 'f1'
    elif 'regression' in id:
        eval_config["config"]["type"] = 'regression'
        eval_config["config"]['metric'] = 'r2'
    elif 'cluster' in id:
        eval_config["config"]["type"] = 'cluster'
        eval_config["config"]['metric'] = 'silhouette'
    else: 
        failed_id.append(id)
        continue
    eval_config['id'] = id
    eval_config['result'][0]['file'] = file
    eval_configs.append(eval_config)


with jsonlines.open('./benchmark/configs/evaluation_ML.jsonl', mode='w') as writer:
    for item in eval_configs:
        writer.write(item)

fails = {"fails": failed_id}
with open('./benchmark/configs/failsML.json', 'w') as f:
    json.dump(fails, f)




    

