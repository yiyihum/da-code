import os, shutil

gold_dir = "/Users/stewiepeter/Desktop/VsProjects/VaftBench/da-code/da_code/gold"
source_dir = "/Users/stewiepeter/Desktop/VsProjects/VaftBench/da-code/da_code/source"

gold_id = os.listdir(gold_dir)
source_id = os.listdir(source_dir)


src_gold = "/Users/stewiepeter/Desktop/VsProjects/DA-Code/dabench/gold"
src_source = "/Users/stewiepeter/Desktop/VsProjects/DA-Code/dabench/source"


for gold in gold_id:
    tgt_gold = os.path.join(gold_dir, gold)
    tgt_source = os.path.join(source_dir, gold)
    shutil.rmtree(tgt_gold)
    shutil.rmtree(tgt_source)
    
    src_gold_file = os.path.join(src_gold, gold)
    src_source_file = os.path.join(src_source, gold)
    
    shutil.copytree(src_gold_file, tgt_gold)
    shutil.copytree(src_source_file, tgt_source)