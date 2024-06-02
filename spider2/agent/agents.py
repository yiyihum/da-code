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
from spider2.agent.prompts import SYS_PROMPT_IN_OUR_CODE, SYS_PROMPT_OUTPUT_FORMAT
from spider2.agent.action import ExecuteCode, CreateFile, Action, Terminate, EditFile
from spider2.envs.spider2 import Spider2Env
from openai import AzureOpenAI
from typing import Dict, List, Optional, Tuple, Any, TypedDict

from agent.models import call_llm

# TODO: 
# add time limit for each action ✅
# add length limit for each ovbservation  ✅
# process contant policy violation ⭕️
# process massage too long ⭕️
# create file & edit 加一个检查 比如符合csv的格式 ✅
# - edit line of file ❌

MAX_OBSERVATION_LENGTH = 2000
TIME_OUT_ACTION = 30


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
        self.env = None

        self._AVAILABLE_ACTION_CLASSES = [ExecuteCode, CreateFile, EditFile, Terminate]
        # self._AVAILABLE_ACTION_CLASSES = [ExecuteCode, Terminate]
        self.work_dir = "/workspace"
        
    def set_env_and_task(self, env: Spider2Env):
        self.env = env
        self.thoughts = []
        self.actions = []
        self.observations = []
        self.instruction = self.env.task_config['instruction']
        action_space = "".join([action_cls.get_action_description() for action_cls in self._AVAILABLE_ACTION_CLASSES])
        self.system_message = SYS_PROMPT_IN_OUR_CODE.format(work_dir=self.work_dir, action_space=action_space) + "\n" + SYS_PROMPT_OUTPUT_FORMAT + "\n  The user asked the following question: # TASK # \n {}".format(self.instruction)
        
    def predict(self, obs: Dict=None) -> List:
        """
        Predict the next action(s) based on the current observation.
        """    
        
        messages = []
        masks = None
        
        messages.append({
            "role": "system",
            "content": [
                {
                    "type": "text",
                    "text": self.system_message 
                },
            ]
        })
        
        assert len(self.observations) == len(self.actions) and len(self.actions) == len(self.thoughts) \
            , "The number of observations and actions should be the same."
            
        if len(self.observations) > self.max_memory_length:
            if self.max_memory_length == 0:
                _observations = []
                _actions = []
                _thoughts = []
            else:
                _observations = self.observations[-self.max_memory_length:]
                _actions = self.actions[-self.max_memory_length:]
                _thoughts = self.thoughts[-self.max_memory_length:]
        else:
            _observations = self.observations
            _actions = self.actions
            _thoughts = self.thoughts
            
        for previous_obs, previous_action, previous_thought in zip(_observations, _actions, _thoughts):
            
            messages.append({
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": """Given the observation as below:\n{}\nWhat's the next step that you will do to help with the task?""".format(
                            previous_obs)
                    }
                ]
            })
            
            messages.append({
                "role": "assistant",
                "content": [
                    {
                        "type": "text",
                        "text": "thought and action: {}".format(previous_thought.strip() if len(previous_thought) > 0 else "No valid thought")
                    },
                ]
            })
            
        if obs is not None:
            self.observations.append(obs)            
            messages.append({
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Observation: {}\n".format(str(obs))
                    }
                ]
            })            

        response = call_llm({
            "model": self.model,
            "messages": messages,
            "max_tokens": self.max_tokens,
            "top_p": self.top_p,
            "temperature": self.temperature
        })
        
        logger.info("RESPONSE: %s", response)

        try:
            action = self.parse_action(response)
            self.thoughts.append(response)
        except ValueError as e:
            print("Failed to parse action from response", e)
            action = None
            self.thoughts.append("")
        
        return response, action
    
    
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
        if action_string == "":
            action_string = output.strip()
        
        output_action = None
        for action_cls in self._AVAILABLE_ACTION_CLASSES:
            action = action_cls.parse_action_from_text(action_string)
            if action is not None:
                output_action = action
        # TODO: add a default action if no action is parsed
        if output_action is None:
            output_action = ExecuteCode(code=action_string)
        
        self.actions.append(output_action)
        return output_action
    

    
    def run(self):
        assert self.env is not None, "Environment is not set."

        done = False
        step_idx = 0
        obs = "You are in the folder now."

        while not done and step_idx < self.max_steps:

            response, action = self.predict(
                obs
            )

            logger.info("Step %d: %s", step_idx + 1, action)

            obs, done = self.env.step(action)

            if done:
                logger.info("The task is done.")
                break
            step_idx += 1

        return done

    def get_trajectory(self):
        trajectory = []
        for i in range(len(self.observations)):
            trajectory.append({
                "observation": self.observations[i],
                "action": str(self.actions[i]),
                "thought": self.thoughts[i]
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
