import jsonlines

# 定义源文件和目标文件的路径
source_file = 'benchmark/configs/Visual.jsonl'
target_file = 'benchmark/configs/Verbose.jsonl'

# 读取源文件内容
with jsonlines.open(source_file) as reader:
    source_data = [obj for obj in reader if obj["hardness"] == "Hard"]

# 追加到目标文件
with jsonlines.open(target_file, mode='a') as writer:
    writer.write_all(source_data)

print("内容已成功追加到目标文件中。")