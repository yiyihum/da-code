import shutil
import os

def move_files(src_dir, dest_dir):
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)
    for filename in os.listdir(src_dir):
        src_file = os.path.join(src_dir, filename)
        dest_file = os.path.join(dest_dir, filename)
        shutil.move(src_file, dest_file)

base_src_dir = "./benchmark/source/"
base_dest_dir = "./benchmark/gold"
names = os.listdir(base_src_dir)  # 获取所有的名称

for name in names:
    src_dir = os.path.join(base_src_dir, name, "gold")
    if not os.path.exists(src_dir):
        continue
    dest_dir = os.path.join(base_dest_dir, name)
    if not os.path.exists(dest_dir):
        move_files(src_dir, dest_dir)
    os.removedirs(src_dir)
    