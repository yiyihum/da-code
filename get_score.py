import json
import glob
import pandas as pd
import numpy as np


model_names = ["gpt4-turbo","claude-3-opus-20240229","gemini-1.5-pro-latest","llama3-70b","qwen-max","Mixtral-8x22B-Instruct-v0.1","deepseek-coder-33b-instruct","CodeLlama-70b-Instruct-hf","mixtral-8x7b-32768"]
model_results = {}

df = pd.DataFrame(np.zeros((len(model_names), 6)), columns=["dw","ml","plot","dm","sa","total"], index=model_names)
for model in model_names:
    task_results = []
    hardness_results = []
    with open(f"benchmark/results/{model}_result.json") as f:
        data = json.load(f)
        task_results.extend(data["results"])
    len_task = {"dw":0,"ml":0,"plot":0,"dm":0,"sa":0}
    len_hardness = {"Easy":0,"Medium":0,"Hard":0,"none":0}
    for task in task_results:
        for key in len_task.keys():
            if task["id"].startswith(key) or (key == "sa" and task["id"].startswith("data-sa")):
                len_task[key] += 1
                break
        for key in len_hardness.keys():
            if task["hardness"] == key:
                len_hardness[key] += 1
                break
        
    print(f"{model}: {sum(len_task.values())}")
    # len_task 保存为csv
    df.loc[model,"dw"] = len_task["dw"]
    df.loc[model,"ml"] = len_task["ml"]
    df.loc[model,"plot"] = len_task["plot"]
    df.loc[model,"dm"] = len_task["dm"]
    df.loc[model,"sa"] = len_task["sa"]
    df.loc[model,"total"] = sum(len_task.values())
    model_results[model] = task_results

print(f"task saved to results/task.csv")
df.to_csv(f"results/task.csv", float_format='%d')

keys = ["total_score","finished","steps"]
for key in keys:
    #建立一个二维表格，行是模型，列是任务&average
    df = pd.DataFrame(np.zeros((len(model_names), 5)), columns=["DW","EDA","ML","macro_average","micro_average"], index=model_names)
    for model in model_names:
        task_results = model_results[model]
        dw = []
        eda = []
        ml = []
        for task in task_results:
            if task["id"].startswith("dw"):
                dw.append(float(task[key]))
            elif task["id"].startswith("ml"):
                ml.append(float(task[key]))
            else:
                eda.append(float(task[key]))

        if len(dw)==0:
            dw = [0]
        if len(eda)==0:
            eda = [0]
        if len(ml)==0:
            ml = [0]
        df.loc[model,"DW"] = sum(dw)/len(dw)
        df.loc[model,"EDA"] = sum(eda)/len(eda)
        df.loc[model,"ML"] = sum(ml)/len(ml)
        df.loc[model,"macro_average"] = (sum(dw)/len(dw) + sum(eda)/len(eda) + sum(ml)/len(ml))/3
        df.loc[model,"micro_average"] = sum(dw+eda+ml)/len(dw+eda+ml)

    print(f"{key} saved to results/{key}.csv")
    df.to_csv(f"results/{key}.csv", float_format='%.3f')

# hardness_result
df = pd.DataFrame(np.zeros((len(model_names), 4)), columns=["Easy","Medium","Hard","none"], index=model_names)
for model in model_names:
    task_results = model_results[model]
    easy = []
    medium = []
    hard = []
    none = []
    for task in task_results:
        if task["hardness"] == "Easy":
            easy.append(int(task[key]))
        elif task["hardness"] == "Medium":
            medium.append(int(task[key]))
        elif task["hardness"] == "Hard":
            hard.append(int(task[key]))
        else:
            none.append(int(task[key]))

    if len(easy)==0:
        easy = [0]
    if len(medium)==0:
        medium = [0]
    if len(hard)==0:
        hard = [0]
    if len(none)==0:
        none = [0]
    df.loc[model,"Easy"] = sum(easy)/len(easy)
    df.loc[model,"Medium"] = sum(medium)/len(medium)
    df.loc[model,"Hard"] = sum(hard)/len(hard)
    df.loc[model,"none"] = sum(none)/len(none)

print(f"hardness saved to results/hardness.csv")
df.to_csv(f"results/hardness.csv", float_format='%.3f')