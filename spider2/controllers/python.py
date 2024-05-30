import json
import logging
import random
from typing import Any, Dict, Optional
import docker
import requests
import os

logger = logging.getLogger("spider.pycontroller")


class PythonController:
    def __init__(self, container, work_dir="/workspace"):
        self.container = container
        self.mnt_dir = [mount['Source'] for mount in container.attrs['Mounts']][0]
        self.work_dir = work_dir
        
        
    def get_file(self, file_path: str):
        """
        Gets a file from the docker container.
        """    
        real_file_path = os.path.join(self.mnt_dir, file_path.replace("/workspace/",""))
        try:
            with open(real_file_path, 'r') as file:
                file_content = file.read()
        except FileNotFoundError:
            print("File not found:", file_path)
        except Exception as e:
            print("An error occurred:", str(e))
        return file_content
    
    def execute_command(self, command: str):
        cmd = ["bash", "-c", command]
        exit_code, output = self.container.exec_run(cmd, workdir=self.work_dir)
        is_cd_flag = command.strip().startswith("cd ")
        if is_cd_flag:
            changed = command[command.index("cd ") + 3:].strip()
            if "&&" in changed:
                changed = changed[:changed.index("&&")].strip()
            self.work_dir = self.update_working_directory(self.work_dir, changed)
            return f"The command to change directory to {self.work_dir} is executed successfully."
        
        return output.decode("utf-8").strip()
    
    def create_file(self, file_path: str, content: str):
        if not file_path.startswith(self.work_dir): # if the filepath is not absolute path, then it is a relative path
            if file_path.startswith("./"): file_path = file_path[2:]
            file_path = os.path.join(self.work_dir.rstrip('/'), file_path)
        real_file_path = os.path.join(self.mnt_dir, file_path.replace("/workspace/",""))
        with open(real_file_path, 'w', encoding="utf-8") as ofp:
            ofp.write(content)
    
    def get_current_workdir(self):
        return self.work_dir
    
    
    
    def update_working_directory(self, current: str, changed: Optional[str] = None) -> str:
        """ Resolves absolute path from the current working directory path and the argument of the `cd` command
        @args:
            current (str): the current working directory
            changed (Optional[str]): the changed working directory, argument of shell `cd` command
        @return:
            new_path (str): absolute path of the new working directory in the container
        """
        if not changed:
            return current
        if changed[0] == "/":
            current = ""

        path = []
        for segment in (current + "/" + changed).split("/"):
            if segment == "..":
                if path:
                    path.pop()
            elif segment and segment != ".":
                path.append(segment)
        new_path = "/" + "/".join(path)
        return new_path
    
    

if __name__ == '__main__':

    client = docker.from_env()
    container_name = "spider2"
    container = client.containers.get(container_name)
    
    
    
    controller = PythonController(container)
    # output = controller.create_file("models/orders_status.md", "aaaaaa")
    # print(output)
    
    # content = controller.execute_command("cd models")
    # print(content)
    # content = controller.execute_command("ls")
    # print(content)
    