import json
import os
from functools import reduce

source_path = "benchmark/results/gpt4-turbo_result.json"

with open(source_path, 'r') as js:
    result = json.load(js)

results = result["results"]

results = list(filter(lambda x: x["hardness"].lower()=="hard", results))

total_score = 0.0
for i in results:
    total_score += i["total_score"]
    
    
avg_score = total_score / len(results)
num_results = len(results)


result_dict = {
    "num_results": num_results,
    "average_score": avg_score,
    "results": results
}

with open("benchmark/results/verbose/gpt4_turbo_wo_verbose.json", "w") as js:
    json.dump(result_dict, js, indent=4)
    

ids1 = set([i["id"] for i in results])

with open("/Users/stewiepeter/Desktop/VsProjects/DA-500/dabench/benchmark/results/verbose/gpt4_turbo_with_verbose.json", 'r') as js2:
    results = json.load(js2)

ids2 = set([i["id"] for i in results["results"]])

print(set(ids1 - ids2))