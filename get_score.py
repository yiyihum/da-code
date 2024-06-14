import json
import glob
import pandas as pd
import numpy as np


model_names = ["azure","claude-3-opus-20240229","gemini-1.5-pro-latest","llama3-70b","mixtral-8x7b-32768","qwen-max"]
model_results = {}
for model in model_names:
    task_results = []
    for file in glob.glob(f"benchmark/results/{model}*.json"):
        with open(file) as f:
            data = json.load(f)
            task_results.extend(data["results"])
    len_task = {"dw":0,"ml":0,"plot":0,"dm":0,"sa":0}
    for task in task_results:
        if task["id"].startswith("dw"):
            len_task["dw"] += 1
        elif task["id"].startswith("ml"):
            len_task["ml"] += 1
        elif task["id"].startswith("plot"):
            len_task["plot"] += 1
        elif task["id"].startswith("dm"):
            len_task["dm"] += 1
        elif task["id"].startswith("data-sa"):
            len_task["sa"] += 1
    print(f"{model}: {sum(len_task.values())}")
    print(len_task)   
    model_results[model] = task_results

keys = ["total_score","finished","steps","len_added_files","len_changed_files"]
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
                dw.append(int(task[key]))
            elif task["id"].startswith("ml"):
                ml.append(int(task[key]))
            else:
                eda.append(int(task[key]))

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

