import uuid, os
import jsonlines
import json


def create_uuid(src: str):
    with jsonlines.open(src, 'r') as f:
        lines = [line for line in f]
    tasks = [line["id"] for line in lines]
    uuids = {task: str(uuid.uuid4()) for task in tasks}
    dir_path = os.path.dirname(os.path.abspath(src))
    uuid_path = os.path.join(dir_path, "id2uuid.json")
    with open(uuid_path, 'w') as js:
        json.dump(uuids, js, indent=4)

def add_uuid(uuid_path: str, add_list: list):
    with open(uuid_path, 'r') as f:
        task2uuid = json.load(f)
    uuids = task2uuid.values()
    new_uuids = set()
    while len(new_uuids) < len(add_list):
        new_uuid = str(uuid.uuid4())
        if new_uuid not in uuids:
            task2uuid[add_list[len(new_uuids)]] = new_uuid
            new_uuids.add(new_uuid)
    
    with open(uuid_path, 'w') as f:
        json.dump(task2uuid, f, indent=4)

    
def convert_config_to_uuid(uuid_path: str, src: str):
    with open(uuid_path, 'r') as js:
        task2uuid = json.load(js)
    with jsonlines.open(src, 'r') as f:
        lines = [line for line in f]
    lines = list(map(
        lambda line: {**line, "name": line["id"]},
        lines
    ))
    lines = list(map(
        lambda line: {**line, "id": task2uuid.get(line["name"], line["name"])},
        lines
    ))
    src = os.path.abspath(src)
    tgt = os.path.join(os.path.dirname(src), "uuid_" + os.path.basename(src))
    with jsonlines.open(tgt, 'w') as f:
        f.write_all(lines)

def convert_dirname_to_uuid(uuid_path: str, dir_path: str):
    with open(uuid_path, 'r') as js:
        task2uuid = json.load(js)
    sub_dirs = os.listdir(dir_path)
    for sub_dir in sub_dirs:
        if sub_dir in task2uuid.keys():
            tgt_dir = task2uuid[sub_dir]
        else:
            continue
        src_path = os.path.join(dir_path, sub_dir)
        tgt_path = os.path.join(dir_path, tgt_dir)
        os.rename(src_path, tgt_path)
    
def convert_result_to_uuid(uuid_path: str, src_path:str):
    with open(src_path, 'r') as f:
        results = json.load(f)
    with open(uuid_path, 'r') as js:
        task2uuid = json.load(js)
    
    results["results"] = list(map(
        lambda x: {**x, "name": x["id"]},
        results["results"]
    ))
    results["results"] = list(map(
        lambda x: {**x, "id": task2uuid.get(x["name"], x["name"])},
        results["results"]
    ))
    
    src_path = os.path.abspath(src_path)
    tgt = os.path.join(os.path.dirname(src_path), "uuid_" + os.path.basename(src_path))
    with open(tgt, 'w') as f:
        json.dump(results, f, indent=4)
    
    
uuid_path = './da_code/configs/id2uuid.json'
src = './da_code/configs/examples.jsonl'
dir_path = './output/gpt4'
src_path = "results/gpt4.json"

convert_config_to_uuid(uuid_path, src)
    
            
        
    