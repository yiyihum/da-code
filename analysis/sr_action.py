import json
import glob
import os 
import matplotlib.pyplot as plt
from matplotlib import colors
import seaborn as sns
import matplotlib.lines as mlines

#换一个颜色相差更大的

#E58606,#5D69B1,#52BCA3,#99C945,#CC61B0,#24796C,#DAA51B,#2F8AC4,#764E9F,#ED645A,#CC3A8E,#A5AA99
colorset = ["#E58606","#5D69B1","#52BCA3","#99C945","#CC61B0","#24796C","#DAA51B","#2F8AC4","#764E9F","#ED645A","#CC3A8E","#A5AA99"]

result_folder = '/home/v-yimhuang/dabench/dabench/benchmark/results'

# models = ["Gemini-1.5-pro","Claude-3-opus","Qwen-max","Llama3-70b","CodeLlama-70b","CodeLlama-34b","Deepseek-Coder-33b","Mixtral-8x22B","GPT-4o","GPT-4","GPT-3.5","Qwen2-72B"]
models = ["Gemini-1.5-pro","Claude-3-opus","Qwen-max","Llama3-70b","Deepseek-Coder-33b","Mixtral-8x22B","GPT-4o","GPT-4","GPT-3.5","Qwen2-72B"]

models_results = {}

for model in models:
    finished = [0]*21
    success = [0]*21
    result_file = glob.glob(os.path.join(result_folder, f'{model}*_result.json'))[0]
    with open(result_file, 'r') as file:
        data_results = json.load(file)["results"]
    for data_result in data_results:
        if data_result["total_score"] > 0:
            success[data_result["steps"]] += 1
        if data_result["finished"]:
            finished[data_result["steps"]] += 1
    #累计
    for i in range(1, 21):
        success[i] += success[i-1]
        finished[i] += finished[i-1]
    #计算比例
    total = len(data_results)
    success_rate = [round(s/total, 3) for s in success]
    unfinished_rate = [round((total-f)/total, 3) for f in finished]
    models_results[model] = {"success_rate": success_rate, "unfinished_rate": unfinished_rate, "final_success_rate": success_rate[-1]}

# sort by final success rate
models_results = dict(sorted(models_results.items(), key=lambda item: item[1]["final_success_rate"], reverse=True))

# Setup for the plot
steps = list(range(21))
fig, ax1 = plt.subplots(figsize=(8, 6))
ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

i = 0
for model, rates in models_results.items():
    color = colorset[i]
    ax1.plot(steps, rates['unfinished_rate'], '--', color=color, alpha=0.5)
    ax2.plot(steps, rates['success_rate'], '-', color=color)
    ax2.plot(20, rates['final_success_rate'], '*', color=color, markersize=10, label=f"{model}")
    i += 1

# Labels and titles
ax1.set_xlabel('Step')
ax1.set_ylabel('Uncompletion Rate (%)')
ax2.set_ylabel('Success Ratio (%)')
ax2.set_ylim(0, 0.6)

# Custom legend handles
success_line = mlines.Line2D([], [], color='black', markersize=10, label='Success Rate', linestyle='-')
unfinished_line = mlines.Line2D([], [], color='black', label='Uncompletion Rate',
                                 linestyle='--')

ax1.set_title('Model Performance Over Steps', fontsize=16)
# fig.tight_layout()

ax1.set_ylim(0, 1.05)
ax1.set_xticks(steps)




lines2, labels2 = ax2.get_legend_handles_labels()
# Legend setup: adding custom entries
ax2.legend(handles=[success_line, unfinished_line] + lines2, loc='center left', fontsize=8)



#设置字体大小
# Show the plot
plt.savefig("./Model_Performance_Over_Steps.pdf", bbox_inches='tight')