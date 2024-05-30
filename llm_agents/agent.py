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
from llm_agents.prompts import SYS_PROMPT_IN_OUR_CODE, SYS_PROMPT_OUTPUT_FORMAT
from llm_agents.action import ExecuteCode, CreateFile, Action, Terminate, EditFile
from spider2.envs.spider2 import Spider2Env
from openai import AzureOpenAI
from typing import Dict, List, Optional, Tuple, Any, TypedDict


import google.generativeai as genai
import openai
import requests
import tiktoken


logger = logging.getLogger("spider2")

# TODO: 
# add time limit for each action
# add length limit for each ovbservation  eg. awk 'NR>=10 && NR<=20' test.csv
# process contant policy violation
# create file & edit 加一个检查 比如符合csv的格式
# - edit line of file


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
        self.system_message = SYS_PROMPT_IN_OUR_CODE.format(work_dir=self.work_dir, action_space=action_space) + "\n" + SYS_PROMPT_OUTPUT_FORMAT + "\nYou are asked to complete the following task: {}".format(self.instruction)
        
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
                        "text": "Given the environment and info as below:\n{}\nWhat's the next step that you will do to help with the task?".format(
                            previous_obs)
                    }
                ]
            })
            
            messages.append({
                "role": "assistant",
                "content": [
                    {
                        "type": "text",
                        "text": previous_thought.strip() if len(previous_thought) > 0 else "No valid action"
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

        response = self.call_llm({
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
        action_string = ""
        patterns = [r'Action: (.*?)Observation', r'Action: (.*?)$', r'^(.*?)Observation']
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

            obs, done = self.step(action)

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
    def call_llm(self, payload):

        if self.model.startswith("gpt"):
        
            
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {os.environ['OPENAI_API_KEY']}"
            }
            logger.info("Generating content with GPT model: %s", self.model)
            response = requests.post(
                "https://api.openai.com/v1/chat/completions",
                headers=headers,
                json=payload
            )
            if response.status_code != 200:
                if response.json()['error']['code'] == "context_length_exceeded":
                    logger.error("Context length exceeded. Retrying with a smaller context.")
                    payload["messages"] = [payload["messages"][0]] + payload["messages"][-1:]
                    retry_response = requests.post(
                        "https://api.openai.com/v1/chat/completions",
                        headers=headers,
                        json=payload
                    )
                    if retry_response.status_code != 200:
                        logger.error(
                            "Failed to call LLM even after attempt on shortening the history: " + retry_response.text)
                        return ""

                logger.error("Failed to call LLM: " + response.text)
                time.sleep(5)
                # logger.info(f"Input: \n{payload['messages']}\nOutput:{response.text}")
                return ""
            else:
                output_message = response.json()['choices'][0]['message']['content']
                # logger.info(f"Input: \n{payload['messages']}\nOutput:{output_message}")
                return output_message

        elif self.model.startswith("azure"):
            
            client = AzureOpenAI(
                api_key = os.environ['AZURE_API_KEY'],  
                api_version = "2024-02-15-preview",
                azure_endpoint = "https://gpt4caxu.openai.azure.com/"
            )
            for i in range(5):
                try:
                    response = client.chat.completions.create(model='gpt4turbo',messages=payload['messages'], max_tokens=payload['max_tokens'], top_p=payload['top_p'], temperature=payload['temperature'])
                    response = response.choices[0].message.content
                    # logger.info(f"Input: \n{payload['messages']}\nOutput:{response}")
                    break
                except Exception as e:
                    logger.error("Failed to call LLM: " + str(e))
                    error_info = e.response.json()  # 假设异常对象有 response 属性并包含 JSON 数据
                    code_value = error_info['error']['code']
                    if code_value == "content_filter":
                        response = error_info['error']['message']
                    else:
                        logger.error("Retrying ...")
                        time.sleep(10 * (2 ** (i + 1)))
                        response = ""
            return response

        elif self.model.startswith("claude"):
            messages = payload["messages"]
            max_tokens = payload["max_tokens"]
            top_p = payload["top_p"]
            temperature = payload["temperature"]

            claude_messages = []

            for i, message in enumerate(messages):
                claude_message = {
                    "role": message["role"],
                    "content": []
                }
                assert len(message["content"]) in [1, 2], "One text, or one text with one image"
                for part in message["content"]:

                    if part['type'] == "image_url":
                        image_source = {}
                        image_source["type"] = "base64"
                        image_source["media_type"] = "image/png"
                        image_source["data"] = part['image_url']['url'].replace("data:image/png;base64,", "")
                        claude_message['content'].append({"type": "image", "source": image_source})

                    if part['type'] == "text":
                        claude_message['content'].append({"type": "text", "text": part['text']})

                claude_messages.append(claude_message)

            # the claude not support system message in our endpoint, so we concatenate it at the first user message
            if claude_messages[0]['role'] == "system":
                claude_system_message_item = claude_messages[0]['content'][0]
                claude_messages[1]['content'].insert(0, claude_system_message_item)
                claude_messages.pop(0)

            logger.debug("CLAUDE MESSAGE: %s", repr(claude_messages))

            headers = {
                "x-api-key": os.environ["ANTHROPIC_API_KEY"],
                "anthropic-version": "2023-06-01",
                "content-type": "application/json"
            }

            payload = {
                "model": self.model,
                "max_tokens": max_tokens,
                "messages": claude_messages,
                "temperature": temperature,
                "top_p": top_p
            }

            response = requests.post(
                "https://api.anthropic.com/v1/messages",
                headers=headers,
                json=payload
            )

            if response.status_code != 200:

                logger.error("Failed to call LLM: " + response.text)
                time.sleep(5)
                return ""
            else:
                return response.json()['content'][0]['text']

        elif self.model.startswith("mistral"):
            messages = payload["messages"]
            max_tokens = payload["max_tokens"]
            top_p = payload["top_p"]
            temperature = payload["temperature"]

            mistral_messages = []

            for i, message in enumerate(messages):
                mistral_message = {
                    "role": message["role"],
                    "content": ""
                }

                for part in message["content"]:
                    mistral_message['content'] = part['text'] if part['type'] == "text" else ""

                mistral_messages.append(mistral_message)

            from openai import OpenAI

            client = OpenAI(api_key=os.environ["TOGETHER_API_KEY"],
                            base_url='https://api.together.xyz',
                            )
            logger.info("Generating content with Mistral model: %s", self.model)

            flag = 0
            while True:
                try:
                    if flag > 20: break
                    response = client.chat.completions.create(
                        messages=mistral_messages,
                        model=self.model,
                        max_tokens=max_tokens,
                        top_p=top_p,
                        temperature=temperature
                    )
                    break
                except:
                    if flag == 0:
                        mistral_messages = [mistral_messages[0]] + mistral_messages[-1:]
                    else:
                        mistral_messages[-1]["content"] = ' '.join(mistral_messages[-1]["content"].split()[:-500])
                    flag = flag + 1

            try:
                return response.choices[0].message.content
            except Exception as e:
                print("Failed to call LLM: " + str(e))
                return ""

        elif self.model.startswith("THUDM"):
            # THUDM/cogagent-chat-hf
            messages = payload["messages"]
            max_tokens = payload["max_tokens"]
            top_p = payload["top_p"]
            temperature = payload["temperature"]

            cog_messages = []

            for i, message in enumerate(messages):
                cog_message = {
                    "role": message["role"],
                    "content": []
                }

                for part in message["content"]:
                    if part['type'] == "image_url":
                        cog_message['content'].append(
                            {"type": "image_url", "image_url": {"url": part['image_url']['url']}})

                    if part['type'] == "text":
                        cog_message['content'].append({"type": "text", "text": part['text']})

                cog_messages.append(cog_message)

            # the cogagent not support system message in our endpoint, so we concatenate it at the first user message
            if cog_messages[0]['role'] == "system":
                cog_system_message_item = cog_messages[0]['content'][0]
                cog_messages[1]['content'].insert(0, cog_system_message_item)
                cog_messages.pop(0)

            payload = {
                "model": self.model,
                "max_tokens": max_tokens,
                "messages": cog_messages,
                "temperature": temperature,
                "top_p": top_p
            }

            base_url = "http://127.0.0.1:8000"

            response = requests.post(f"{base_url}/v1/chat/completions", json=payload, stream=False)
            if response.status_code == 200:
                decoded_line = response.json()
                content = decoded_line.get("choices", [{}])[0].get("message", "").get("content", "")
                return content
            else:
                print("Failed to call LLM: ", response.status_code)
                return ""

        elif self.model.startswith("gemini"):
            def encoded_img_to_pil_img(data_str):
                base64_str = data_str.replace("data:image/png;base64,", "")
                image_data = base64.b64decode(base64_str)
                image = Image.open(BytesIO(image_data))

                return image

            messages = payload["messages"]
            max_tokens = payload["max_tokens"]
            top_p = payload["top_p"]
            temperature = payload["temperature"]

            gemini_messages = []
            for i, message in enumerate(messages):
                role_mapping = {
                    "assistant": "model",
                    "user": "user",
                    "system": "system"
                }
                gemini_message = {
                    "role": role_mapping[message["role"]],
                    "parts": []
                }
                assert len(message["content"]) in [1, 2], "One text, or one text with one image"

                # The gemini only support the last image as single image input
                if i == len(messages) - 1:
                    for part in message["content"]:
                        gemini_message['parts'].append(part['text']) if part['type'] == "text" \
                            else gemini_message['parts'].append(encoded_img_to_pil_img(part['image_url']['url']))
                else:
                    for part in message["content"]:
                        gemini_message['parts'].append(part['text']) if part['type'] == "text" else None

                gemini_messages.append(gemini_message)

            # the mistral not support system message in our endpoint, so we concatenate it at the first user message
            if gemini_messages[0]['role'] == "system":
                gemini_messages[1]['parts'][0] = gemini_messages[0]['parts'][0] + "\n" + gemini_messages[1]['parts'][0]
                gemini_messages.pop(0)

            # since the gemini-pro-vision donnot support multi-turn message
            if self.model == "gemini-pro-vision":
                message_history_str = ""
                for message in gemini_messages:
                    message_history_str += "<|" + message['role'] + "|>\n" + message['parts'][0] + "\n"
                gemini_messages = [{"role": "user", "parts": [message_history_str, gemini_messages[-1]['parts'][1]]}]
                # gemini_messages[-1]['parts'][1].save("output.png", "PNG")

            # print(gemini_messages)
            api_key = os.environ.get("GENAI_API_KEY")
            assert api_key is not None, "Please set the GENAI_API_KEY environment variable"
            genai.configure(api_key=api_key)
            logger.info("Generating content with Gemini model: %s", self.model)
            request_options = {"timeout": 120}
            gemini_model = genai.GenerativeModel(self.model)
            try:
                response = gemini_model.generate_content(
                    gemini_messages,
                    generation_config={
                        "candidate_count": 1,
                        "max_output_tokens": max_tokens,
                        "top_p": top_p,
                        "temperature": temperature
                    },
                    safety_settings={
                        "harassment": "block_none",
                        "hate": "block_none",
                        "sex": "block_none",
                        "danger": "block_none"
                    },
                    request_options=request_options
                )
                return response.text
            except Exception as e:
                logger.error("Meet exception when calling Gemini API, " + str(e.__class__.__name__) + str(e))
                logger.error(f"count_tokens: {gemini_model.count_tokens(gemini_messages)}")
                logger.error(f"generation_config: {max_tokens}, {top_p}, {temperature}")
                return ""
        elif self.model.startswith("qwen"):
            messages = payload["messages"]
            max_tokens = payload["max_tokens"]
            top_p = payload["top_p"]
            if payload["temperature"]:
                logger.warning("Qwen model does not support temperature parameter, it will be ignored.")

            qwen_messages = []

            for i, message in enumerate(messages):
                qwen_message = {
                    "role": message["role"],
                    "content": []
                }
                assert len(message["content"]) in [1, 2], "One text, or one text with one image"
                for part in message["content"]:
                    qwen_message['content'].append({"image": part['image_url']['url']}) if part[
                                                                                               'type'] == "image_url" else None
                    qwen_message['content'].append({"text": part['text']}) if part['type'] == "text" else None

                qwen_messages.append(qwen_message)

            response = dashscope.MultiModalConversation.call(
                model='qwen-vl-plus',
                messages=messages,
                max_length=max_tokens,
                top_p=top_p,
            )
            # The response status_code is HTTPStatus.OK indicate success,
            # otherwise indicate request is failed, you can get error code
            # and message from code and message.
            if response.status_code == HTTPStatus.OK:
                try:
                    return response.json()['output']['choices'][0]['message']['content']
                except Exception:
                    return ""
            else:
                print(response.code)  # The error code.
                print(response.message)  # The error message.
                return ""

        else:
            raise ValueError("Invalid model: " + self.model)
        
        
    def step(self, action: Action):
        
        done = False
        if isinstance(action, ExecuteCode):
            observation = self.execute_code_action(action)
        elif isinstance(action, CreateFile):
            observation = self.create_file_action(action)
        elif isinstance(action, EditFile):
            observation = self.edit_file_action(action)
        elif isinstance(action, Terminate):
            observation = "Terminate"
            done = True
        else:
            raise ValueError(f"Unrecognized action type {action.action_type} !")
        logger.info("Observation: %s", observation)
        return observation, done
        
        
        
    def create_file_action(self, action: CreateFile):
        try:
            self.env.controller.create_file(action.filepath, action.code)
        except:
            obs = f"Failed to create file in {action.filepath}",
        else:
            obs = f"File created successfully in {action.filepath}"
        return obs


    def execute_code_action(self, action: ExecuteCode):
        """ Execute action in bash shell """
        
        obs = self.env.controller.execute_command(action.code)
        if obs is None or obs == '':
            obs = "code executed successfully."
        
        return obs
    
    
    def edit_file_action(self, action: EditFile):
        self.env.controller.execute_command(f"rm {action.filepath}")
        try:
            self.env.controller.create_file(action.filepath, action.code)
        except:
            obs = f"Failed to edit file in {action.filepath}",
        else:
            obs = f"File edit successfully in {action.filepath}"
        return obs