import signal
import os
import hashlib
import shutil
from typing import Dict


TIMEOUT_DURATION = 25

class timeout:
    def __init__(self, seconds=TIMEOUT_DURATION, error_message="Timeout"):
        self.seconds = seconds
        self.error_message = error_message

    def handle_timeout(self, signum, frame):
        raise TimeoutError(self.error_message)

    def __enter__(self):
        signal.signal(signal.SIGALRM, self.handle_timeout)
        signal.alarm(self.seconds)

    def __exit__(self, type, value, traceback):
        signal.alarm(0)


def delete_files_in_folder(folder_path):
    if os.path.exists(folder_path):
        files = os.listdir(folder_path)
        for file in files:
            file_path = os.path.join(folder_path, file)
            if os.path.isfile(file_path):
                os.remove(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        
def create_folder_if_not_exists(path):
    if not os.path.exists(path):
        os.makedirs(path)

def calculate_sha256(file_path):
    with open(file_path, 'rb') as f:
        file_data = f.read()
        return hashlib.sha256(file_data).hexdigest()


def find_diff_files(dict1, dict2)-> Dict:
    added_files = set(dict2.keys()) - set(dict1.keys())
    changed_files = {k: dict2[k] for k in set(dict1.keys()) & set(dict2.keys()) if dict1[k] != dict2[k]}
    added_files_list = list(added_files)
    changed_files_list = list(changed_files.keys())
    return {"added_files": added_files_list, "changed_files": changed_files_list}
