import logging
import os
import subprocess
import tempfile
import time
from typing import Callable, Any, Optional, Tuple

from typing import List, Dict, Union
from docker.models.containers import Container
from docker.client import DockerClient
from docker.errors import ImageNotFound
import gymnasium as gym
import shutil, pathlib, docker, time, copy
from spider2.controllers.python import PythonController
from spider2.controllers.setup import SetupController
from spider2.envs.utils import *
from spider2 import configs
from spider2.agent.action import ExecuteBash, CreateFile, Action, Terminate, EditFile, ExecutePythonSnippet
import signal

logger = logging.getLogger("spider2.env")

Metric = Callable[[Any, Any], float]
Getter = Callable[[gym.Env, Dict[str, Any]], Any]


# constants
START_UP_DELAY = 2 # start up delay for docker container
DEFAULT_TIME_OUT = 20 # default waiting time for each action
MAX_OBS_LENGTH = 3000
EMPTY_DATA_PATH = 'benchmark/data/empty' # an empty data directory
DEFAULT_IMAGE_DIR = 'benchmark/images' # default directory to store docker images
DEFAULT_WORK_DIR = '/workspace' # default working directory in the container
DEFAULT_MNT_DIR = 'benchmark/mnt' # default directory to copy and mount data path, also the output directory
TASK_FINISHED = "task_finished" # infos key
ACTION_EXEC = "action_executed" # infos key


class Spider2Env(gym.Env):
    """
    DesktopEnv with OpenAI Gym interface.
    Fixme: refactor the logic when implementing the multi-process version
    """
    def __init__(self, env_config, task_config, cache_dir, mnt_dir):
        """
        Args:
            path_to_vm (str): path to .vmx file
            action_space (str): "computer_13" | "pyautogui"

            task_config (Dict[str, Any]): manages task configs integratedly,
              including
              * base snapshot
              * task id (uuid)
              * instruction
              * setup config

            tmp_dir (str): temporary directory to store trajectory stuffs like
              the extracted screenshots
            cache_dir (str): cache directory to cache task-related stuffs like
              reference file for evaluation
        """
        super().__init__()
        self.task_config = task_config
        self.cache_dir_base = cache_dir
        self.container_name = env_config['init_args']['name']
        self.image_name = env_config['image_name']
        self.mnt_dir = mnt_dir
        self.work_dir = DEFAULT_WORK_DIR
        self.kwargs = env_config['init_args']

        self._set_task_info(task_config)
        logger.info("Initializing...")
        self._construct_container()
        
        self.controller = PythonController(container=self.container, work_dir=self.work_dir)
        self.setup_controller = SetupController(container=self.container, cache_dir=self.cache_dir)
        
        logger.info("Setting up environment...")
        self.setup_controller.setup(self.config)
        self.init_files_hash = self._get_env_files_hash()
        time.sleep(2)
        logger.info("Environment setup complete.")
        
        
        
    def _set_task_info(self, task_config: Dict[str, Any]):
        self.task_id: str = task_config['id']
        self.cache_dir: str = os.path.join(self.cache_dir_base, self.task_id)
        os.makedirs(self.cache_dir, exist_ok=True)
        self.instruction = task_config["instruction"]
        self.config = task_config["config"] if "config" in task_config else []
        self.post_process_func = task_config["post_process"] if "post_process" in task_config else []


        # evaluator dict
        # func -> metric function string, or list of metric function strings
        # conj -> conjunction of multiple metrics if func is a list with length > 1, "and"/"or"
        # result -> result getter config, or list of result getter configs
        # expected (optional) -> expected getter config, or list of expected getter configs
        # options (optional) -> metric options, or list of metric options
        # if func is a str list, then result, expected (if exists), options (if exists) should also be lists of the same length
        # even if one of the metrics does not need expected or options field, it should be included in the list with None
        # self.evaluator = task_config["evaluator"]
        # self.metric: Metric = [getattr(metrics, func) for func in self.evaluator["func"]] \
        # if isinstance(self.evaluator["func"], list) \
        # else getattr(metrics, self.evaluator["func"])
        # self.metric_conj: str = self.evaluator.get("conj", "and")  # take conjunction of multiple metrics
        
        
        # if "result" in self.evaluator:
        #     self.result_getter: Getter = [getattr(getters, "get_{:}".format(res["type"])) for res in
        #                               self.evaluator["result"]] \
        #     if isinstance(self.evaluator["result"], list) \
        #     else getattr(getters, "get_{:}".format(self.evaluator["result"]["type"]))
        # else:
        #     self.result_getter = [None] * len(self.metric) \
        #         if isinstance(self.metric, list) \
        #         else None

        # if "expected" in self.evaluator:
        #     self.expected_getter: Getter = [getattr(getters, "get_{:}".format(exp["type"])) if exp else None for exp in
        #                                     self.evaluator["expected"]] \
        #         if isinstance(self.evaluator["expected"], list) \
        #         else getattr(getters, "get_{:}".format(self.evaluator["expected"]["type"]))
        # else:
        #     self.expected_getter = [None] * len(self.metric) \
        #         if isinstance(self.metric, list) \
        #         else None
        # self.metric_options: Union[List[Dict[str, Any]], Dict[str, Any]] = [opt if opt else {} for opt in
        #                                                                     self.evaluator["options"]] \
        #     if isinstance(self.evaluator.get("options", {}), list) \
        #     else self.evaluator["options"] \
        #     if "options" in self.evaluator \
        #     else [{}] * len(self.metric) \
        #     if isinstance(self.metric, list) \
        #     else {}

        # assert (not isinstance(self.evaluator["func"], list)
        #         or (len(self.metric) == len(self.result_getter) == len(self.expected_getter) == len(
        #             self.metric_options)))
        
        
    def _construct_container(self):
        
        client = docker.from_env()
        container_name = self.container_name
        #### delete existing container
        try:
            container = client.containers.get(container_name)
            container.stop()
            container.remove()
            print(f"Container {container_name} stopped and removed.")
        except docker.errors.NotFound:
            pass
        except docker.errors.APIError as e:
            pass
        
        create_folder_if_not_exists(self.mnt_dir)
        src_dir = pathlib.Path(self.mnt_dir).absolute().__str__()
        delete_files_in_folder(self.mnt_dir)
        
        volumes = {src_dir: {'bind': self.work_dir, 'mode': 'rw'}}
        allowed_params = ['command', 'ports', 'restart_policy', 'entrypoint', 'hostname', 'domainname', 'name', 'user', 'mac_address', 'platform', 'network_mode', 'network_disabled', 'healthcheck', "environment"]
        kwargs = {k: self.kwargs[k] for k in self.kwargs if k in allowed_params}
        extra_params = {'detach': True, 'tty': True, 'stdout': True, 'stderr': True, 'stdin_open': True, **kwargs}

        try:
            client: DockerClient = docker.from_env()
            image = client.images.get(self.image_name)
            self.container: Container = client.containers.run(image=image, volumes=volumes, **extra_params)
        except ImageNotFound as e:
            dockerfile_path = os.path.join(DEFAULT_IMAGE_DIR, self.image_name)
            if os.path.exists(dockerfile_path):
                logger.info(f"Image {self.image_name} not found, try to build from dockerfile {dockerfile_path} ...")
                image = client.images.build(path=dockerfile_path, tag=self.image_name, rm=True)[0]
            else:
                logger.info(f"Image {self.image_name} not found, try to pull from Dockerhub ...")
                image = client.images.pull(self.image_name)[0]
            self.container: Container = client.containers.run(image=image, volumes=volumes, **extra_params)
        except Exception as e:
            logger.info(f"Failed to construct container from image {self.image_name} with error: {e}")
            raise e

        time.sleep(START_UP_DELAY)
        logger.info(f"Connected to container[name={self.container.name}, id={self.container.id}] from image {self.image_name} ...")    
        
        return self.container

    def _get_env_files_hash(self) -> Dict[str, str]:
        """
        Returns:
            Dict[str, str]: a dictionary of the hash of the files in the
              environment
        """
        files_hash = {}
        for root, dirs, files in os.walk(self.mnt_dir):
            for f in files:
                file_path = os.path.join(root, f)
                files_hash[file_path] = calculate_sha256(file_path)
        return files_hash
    
    
    # def setup_config(self):
    #     logger.info("Resetting environment...")
    #     logger.info("Setting up environment...")
    #     self.setup_controller.setup(self.config)
    #     time.sleep(5)
    #     logger.info("Environment setup complete.")
    def post_process(self):
        """
        Evaluate whether the task is successfully completed.
        """
        diff_files = self._find_diff_files_init(self.init_files_hash)

        post_process_files = []
        for post_process_f in self.post_process_func:
            process_function = getattr(configs, post_process_f, None)
            post_files = process_function(self.mnt_dir, self.controller)
            post_files = post_files if isinstance(post_files, list) else list(post_files)
            post_process_files.extend(post_files)

        return {**diff_files, "post_process_files": post_process_files}

    def _find_diff_files_init(self, init_file_dict)-> Dict:
        init_file_paths = init_file_dict.keys()
        added_files_list = []
        changed_files_list = []
        for root, dirs, files in os.walk(self.mnt_dir):
            for f in files:
                file_path = os.path.join(root, f)
                if file_path not in init_file_paths:
                    added_files_list.append(file_path)
                else:
                    if init_file_dict[file_path] != calculate_sha256(file_path):
                        changed_files_list.append(file_path)
        return {"added_files": added_files_list, "changed_files": changed_files_list}
        
    # def evaluate(self):
    #     """
    #     Evaluate whether the task is successfully completed.
    #     """

    #     self.setup_controller.setup(self.evaluator.get("postconfig", []))
    #     if self.metric == "infeasible":
    #         return 0

    #     if type(self.metric) == list:
    #         results = []
    #         for idx, metric in enumerate(self.metric):
    #             try:
    #                 config = self.evaluator["result"][idx]
    #                 result_state = self.result_getter[idx](self, config)
    #                 expected = self.evaluator["expected"][idx]

    #                 expected_state = self.expected_getter[idx](self, expected) if expected else None
    #                 self.metric_options[idx]["mnt_dir"] = self.mnt_dir
    #                 self.metric_options[idx]["controller"] = self.controller
    #                 metric: int = metric(result_state, expected_state,
    #                                     **self.metric_options[idx]) if expected_state is not None \
    #                     else metric(result_state, **self.metric_options[idx])
    #             except FileNotFoundError:
    #                 logger.error("File not found!")
    #                 results.append(0.0)
    #                 continue
    #             results.append(metric)

    #         if self.metric_conj == 'and':
    #             return sum(results) / len(results)
    #         elif self.metric_conj == 'or':
    #             return max(results)
    #     else:
    #         try:
    #             result_state = self.result_getter(self, self.evaluator["result"])
    #         except FileNotFoundError:
    #             logger.error("File not found!")
    #             return 0

    #         expected_state = self.expected_getter(self, self.evaluator["expected"]) if "expected" in self.evaluator \
    #             else None

    #         metric: float = self.metric(result_state, expected_state,
    #                                     **self.metric_options) if expected_state is not None \
    #             else self.metric(result_state, **self.metric_options)

    #     return metric
    
    def step(self, action: Action):
        try:
            with timeout(DEFAULT_TIME_OUT,"Action execution time exceeded!"):
                done = False
                if isinstance(action, ExecuteBash):
                    observation = self.execute_code_action(action)
                elif isinstance(action, CreateFile):
                    observation = self.create_file_action(action)
                elif isinstance(action, EditFile):
                    observation = self.edit_file_action(action)
                elif isinstance(action, ExecutePythonSnippet):
                    observation = self.execute_python_action(action)
                elif isinstance(action, Terminate):
                    observation = "Terminate"
                    done = True
                else:
                    raise ValueError(f"Unrecognized action type {action.action_type} !")
        except TimeoutError as e:
            observation = str(e)
        
        observation = self._handle_observation(observation)
        logger.info("Observation: %s", observation)
        return observation, done
    
    def _handle_observation(self, observation):
        max_length = MAX_OBS_LENGTH  
        if len(observation) > max_length:
            truncated_observation = observation[:max_length] + "\n[Observation too long, truncated; Try other commands to get the left part.]"
            return truncated_observation
        return observation

        
    def create_file_action(self, action: CreateFile):
        obs = self.controller.create_file(action.filepath, action.code)
        if obs is None or obs == '':
            real_file_path = self.controller.get_real_file_path(action.filepath)
            valid, error = is_file_valid(real_file_path)
            if valid:
                obs = f"File {action.filepath} created and written successfully."
            else:
                obs = f"Falied to validate file {action.filepath}, error: {error}"
        return obs


    def execute_code_action(self, action: ExecuteBash):
        """ Execute action in bash shell """
        
        obs = self.controller.execute_command(action.code)
        if obs is None or obs == '':
            obs = "Action executed successfully. No output."
        
        return obs

    def execute_python_action(self, action: ExecutePythonSnippet):
        """ Execute action in python shell """
        obs = self.controller.execute_python_code(action.code)
        if obs is None or obs == '':
            obs = "Action executed successfully. No output."
        
        return obs
    
    
    def edit_file_action(self, action: EditFile):
        obs = self.controller.edit_file(action.filepath, action.code)
        if obs is None or obs == '':
            real_file_path = self.controller.get_real_file_path(action.filepath)
            valid, error = is_file_valid(real_file_path)
            if valid:
                obs = f"File {action.filepath} edited successfully."
            else:
                obs = f"Falied to validate file {action.filepath}, error: {error}"
        return obs
    

    # def step(self, action) -> Tuple[str, float, bool, Dict]:
        
    #     done = False
    #     reward = 0 
        
    #     # handle the special actions
    #     if action in ['WAIT', 'FAIL', 'DONE']:
    #         if action == 'FAIL':
    #             done = True
    #             info = {"fail": True}
    #         elif action == 'DONE':
    #             done = True
    #             info = {"done": True}
        
    #     output = self.controller.execute_command(action)
        
    #     # observation = {
    #     #     ""
    #     #     "output": output,
    #     #     "instruction": self.instruction,
    #     # }
        
    #     return output, reward, done, info
    
    
    
    # def get_environment_description(self) -> str:
    #     """ Return the environment description message.
    #     """
    #     action_space = "".join([action_cls.get_action_description() for action_cls in self._AVAILABLE_ACTION_CLASSES])
    #     return self._ENVIRONMENT_DESCRIPTION.format(work_dir=self.work_dir, action_space=action_space)