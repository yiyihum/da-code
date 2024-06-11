import base64
import json
import logging
import os
import re
import time
import uuid
from http import HTTPStatus
from io import BytesIO
from typing import Dict, List
from spider2.agent.prompts import SYS_PROMPT_IN_OUR_CODE
from spider2.agent.action import Bash, Action, Terminate, Python, SQL
from spider2.envs.spider2 import Spider2Env
from openai import AzureOpenAI
from typing import Dict, List, Optional, Tuple, Any, TypedDict

from agent.models import call_llm

# TODO: 
# add time limit for each action ✅
# add length limit for each ovbservation  ✅
# process contant policy violation ⭕️
# process massage too long ✅
# create file & edit 加一个检查 比如符合csv的格式 ✅

MAX_OBSERVATION_LENGTH = 2000
TIME_OUT_ACTION = 300


logger = logging.getLogger("spider2")


class PromptAgent:
    def __init__(
        self,
        model="gpt-4",
        max_tokens=1500,
        top_p=0.9,
        temperature=0.5,
        max_memory_length=10,
        max_steps=15,
    ):
        
        self.model = model
        self.max_tokens = max_tokens
        self.top_p = top_p
        self.temperature = temperature
        self.max_memory_length = max_memory_length
        self.max_steps = max_steps
        
        self.thoughts = []
        self.actions = []
        self.observations = []
        self.system_message = ""
        self.history_messages = []
        self.env = None
        self.codes = []
        self._AVAILABLE_ACTION_CLASSES = [Bash, Python, SQL, Terminate]
        # self._AVAILABLE_ACTION_CLASSES = [Bash, Terminate]
        self.work_dir = "/workspace"
        
    def set_env_and_task(self, env: Spider2Env):
        self.env = env
        self.thoughts = []
        self.actions = []
        self.observations = []
        self.codes = []
        self.history_messages = []
        self.instruction = self.env.task_config['instruction']
        action_space = "".join([action_cls.get_action_description() for action_cls in self._AVAILABLE_ACTION_CLASSES])
        self.system_message = SYS_PROMPT_IN_OUR_CODE.format(work_dir=self.work_dir, action_space=action_space, task=self.instruction, max_steps=self.max_steps)
        self.history_messages.append({
            "role": "system",
            "content": [
                {
                    "type": "text",
                    "text": self.system_message 
                },
            ]
        })
        
    def predict(self, obs: Dict=None) -> List:
        """
        Predict the next action(s) based on the current observation.
        """    
        
        assert len(self.observations) == len(self.actions) and len(self.actions) == len(self.thoughts) \
            , "The number of observations and actions should be the same."

        status = False
        while not status:
            messages = self.history_messages.copy()
            messages.append({
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Observation: {}\n".format(str(obs))
                    }
                ]
            })  
            status, response = call_llm({
                "model": self.model,
                "messages": messages,
                "max_tokens": self.max_tokens,
                "top_p": self.top_p,
                "temperature": self.temperature
            })
            if not status:
                if response == "context_length_exceeded":
                    self.history_messages = [self.history_messages[0]] + self.history_messages[3:]
                else:
                    raise Exception(f"Failed to call LLM, response: {response}")

        try:
            action = self.parse_action(response)
        except ValueError as e:
            print("Failed to parse action from response", e)
            action = None
        
        logger.info("Observation: %s", obs)
        logger.info("Response: %s", response)

        
        self._add_message(obs, response)
        self.observations.append(obs)
        self.thoughts.append(response)
        self.actions.append(action)
        if action is not None:
            self.codes.append(action.code)
        else:
            self.codes.append(None)

        return response, action
        
    
    def _add_message(self, observations: str, response: str):
        self.history_messages.append({
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "Observation: {}".format(observations)
                }
            ]
        })
        self.history_messages.append({
            "role": "assistant",
            "content": [
                {
                    "type": "text",
                    "text": response
                }
            ]
        })
        if len(self.history_messages) > self.max_memory_length*2+1:
            self.history_messages = [self.history_messages[0]] + self.history_messages[-self.max_memory_length*2:]
    
    def parse_action(self, output: str) -> Action:
        """ Parse action from text """
        if output is None or len(output) == 0:
            pass
        action_string = ""
        patterns = [r'["\']?Action["\']?:? (.*?)Observation', r'["\']?Action["\']?:? (.*?)$', r'^(.*?)Observation']

        for p in patterns:
            match = re.search(p, output, flags=re.DOTALL)
            if match:
                action_string = match.group(1).strip()
                break
        if action_string == "":
            action_string = output.strip()
        
        output_action = None
        for action_cls in self._AVAILABLE_ACTION_CLASSES:
            action = action_cls.parse_action_from_text(action_string)
            if action is not None:
                output_action = action
                break
        if output_action is None:
            action_string = action_string.replace("\_", "_")
            for action_cls in self._AVAILABLE_ACTION_CLASSES:
                action = action_cls.parse_action_from_text(action_string)
                if action is not None:
                    output_action = action
                    break
        
        return output_action
    

    
    def run(self):
        assert self.env is not None, "Environment is not set."
        result = ""
        done = False
        step_idx = 0
        obs = "You are in the folder now."
        retry_count = 0
        last_action = None
        while not done and step_idx < self.max_steps:

            _, action = self.predict(
                obs
            )
            if action is None:
                logger.info("Failed to parse action from response, try again.")
                retry_count += 1
                if retry_count > 3:
                    logger.info("Failed to parse action from response, stop.")
                    break
                obs = "Failed to parse action from your response, make sure you provide a valid action."
            else:
                logger.info("Step %d: %s", step_idx + 1, action)
                if last_action is not None and last_action == action:
                    obs = "The action is the same as the last one, please provide a different action."
                else:
                    obs, done = self.env.step(action)
                    last_action = action

            if done:
                if isinstance(action, Terminate):
                    result = action.output
                logger.info("The task is done.")
                break
            step_idx += 1

        return done, result

    def get_trajectory(self):
        trajectory = []
        for i in range(len(self.observations)):
            trajectory.append({
                "observation": self.observations[i],
                "thought": self.thoughts[i],
                "action": str(self.actions[i]),
                "code": self.codes[i]
            })
        trajectory_log = {
            "Task": self.instruction,
            "system_message": self.system_message,
            "trajectory": trajectory
        }
        return trajectory_log


    
    # @backoff.on_exception(
    #     backoff.expo,
    #     # here you should add more model exceptions as you want,
    #     # but you are forbidden to add "Exception", that is, a common type of exception
    #     # because we want to catch this kind of Exception in the outside to ensure each example won't exceed the time limit
    #     (openai.RateLimitError,
    #      openai.BadRequestError,
    #      openai.InternalServerError,
    #      InvalidArgument),
    #     max_tries=5
    # )

if __name__ == "__main__":
    agent = PromptAgent()
    response = """Thought: The task is to perform a clustering task on the Bank Customer Segmentation dataset to segment the bank customers into an appropriate number of clusters. The dataset is available in the current workspace, and we need to write the clustering results into a file named cluster.csv. \n\nAction: Python(file_name=\"./clustering.py\"):\n```python\nimport pandas as pd\nfrom sklearn.preprocessing import StandardScaler\nfrom sklearn.cluster import KMeans\nimport numpy as np\n\n# Load the dataset\ndata = pd.read_csv('bank_customer_segmentation.csv')\n\n# Preprocess the data\nscaler = StandardScaler()\nprocessed_data = scaler.fit_transform(data)\n\n# Perform K-Means clustering\nkmeans = KMeans(n_clusters=3)  # Assuming 3 clusters for now\nkmeans.fit(processed_data)\n\n# Get the cluster labels\nlabels = kmeans.labels_\n\n# Create a new dataframe with the processed features and cluster labels\ncluster_data = pd.DataFrame(processed_data, columns=[f\"Processed_Feature_{i}\" for i in range(processed_data.shape[1])])\ncluster_data['Cluster'] = labels\n\n# Save the clustering results to a CSV file\ncluster_data.to_csv('cluster.csv', index=False)\n```
"""
    import pdb; pdb.set_trace()
    action = agent.parse_action(response)
    print(action)