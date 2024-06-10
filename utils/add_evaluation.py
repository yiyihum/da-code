import pandas as pd
import jsonlines
import openai,re, os, json
from openai import OpenAI
from tqdm import tqdm
import json
client = OpenAI(
    # This is the default and can be omitted
    api_key=os.environ.get("OPENAI_API_KEY"),
)


model = 'gpt-4'
system_message = """
You are a prompt engineer tasked with helping users extract the output file and evaluation information name from the prompt.

# Objective # 
1. Identify the output file name mentioned in the user's prompt.
2. extraction evaluation configs from instruction, like graph title, x-label, y-label, color


# Response Format #
1. Response must be a json format:
{
    "id": "***",
    "config":{
        "task": "data visualization",
        "type": "***",
        "metric": "",
        "threshold": 0.0
    },
    "func":[
        "compare_image"
    ],
    "result":[
        {   
            "multi": true,
            "file": ["***","dabench/plot.json","dabench/result.npy"]
        }
    ],
    "options": [{
        "keys": ["***"]
    }]
}
2. The id is the task ID mentioned in the instruction, and type is the chart type specified in the instruction, such as "bar","line", "scatter", "pie". The file is the output image file name.
3. The keys represent the graph information mentioned in the instruction.
4.Here are the possible keys:
	•figsize: Shape of the image.
	•labels: Data labels.
	•color: Color.
	•graph_title: Title of the image.
	•legend_title: Title of the legend.
	•x_label: Title of the x-axis.
	•y_label: Title of the y-axis.
	•xtick_labels: Labels for the x-axis ticks.
	•ytick_labels: Labels for the y-axis ticks. 

# Example #
[input]
id: plot-bar-001
instrction: This is a dataset of TV shows on Netflix, Prime Video, Hulu, and Disney+. The relevant description is in README.md. You are required to identify the top ten artists based on sales from this dataset and plot their sales figures in a bar chart. Save the image as sales.jpg, with the title "Top Ten Artists Based on Sales," a size of (6, 6), y-axis labeled as "Artist," and x-axis labeled as "Total Sales."
[output]
{
    "id": "plot-bar-001",
    "config":{
        "task": "data visualization",
        "type": "bar",
        "metric": "",
        "threshold": 0.0
    },
    "func":[
        "compare_image"
    ],
    "result":[
        {   
            "multi": true,
            "file": ["sales.jpg","dabench/plot.json","dabench/result.npy"]
        }
    ],
    "options": [{
        "keys": ["figsize","graph_title", "x_label", "y_label","ytick_labels"]
    }]
}
[input]
id: plot-bar-018
instruction: This is a Kickstarter Projects dataset, with relevant descriptions in the README.md file. You need to calculate the average days to issue for each day of the week and plot the results in a bar chart, saving it as 'result.png'. The chart should have a size of (12, 6), with the title 'Average Days to Issue by Weekday', the x-axis titled 'Weekday', and the y-axis titled 'Average Days to Issue'. The color of the bars should be 'skyblue'.
[output]
{
    "id": "plot-bar-018",
    "config":{
        "task": "data visualization",
        "type": "bar",
        "metric": "",
        "threshold": 0.0
    },
    "func":[
        "compare_image"
    ],
    "result":[
        {   
            "multi": true,
            "file": ["result.png","dabench/plot.json","dabench/result.npy"]
        }
    ],
    "options": [{
        "keys": ["xtick_labels",  "x_label", "y_label", "graph_title", "figsize", "color"]
    }]
}
Now, Let's start.
"""


jsonl_path = './benchmark/configs/Visual.jsonl'
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
    messages.append({"role": 'user','content': f'\n[input]\n"id": {id}\n"instruction": {instruction}'})
    try:
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=0.0, # this is the degree of randomness of the model's output
        )
        response  = response.choices[0].message.content
        pattern = r"\{(.*)\}"
        matches = re.search(pattern, response, re.DOTALL)
        if matches:
            first_match_with_braces = "{" + matches.group(1) + "}"
        else:
            failed_id.append(id)
            continue
        eval_config = json.loads(first_match_with_braces)
    except Exception as e:
        print("id:", e)
        failed_id.append(id)
        continue
    
    eval_configs.append(eval_config)


with jsonlines.open('./benchmark/configs/evaluation_Visual2.jsonl', mode='w') as writer:
    for item in eval_configs:
        writer.write(item)

fails = {"fails": failed_id}
with open('./benchmark/configs/failsV.json', 'w') as f:
    json.dump(fails, f)




    

