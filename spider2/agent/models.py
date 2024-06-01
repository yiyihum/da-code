import base64
import json
import logging
import os
import re
import time
from http import HTTPStatus
from io import BytesIO

from openai import AzureOpenAI
from typing import Dict, List, Optional, Tuple, Any, TypedDict


import google.generativeai as genai
import openai
import requests
import tiktoken
import signal

logger = logging.getLogger("api-llms")


def call_llm(payload):
    model = payload["model"]
    if model.startswith("gpt"):
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {os.environ['OPENAI_API_KEY']}"
        }
        logger.info("Generating content with GPT model: %s", model)
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

    elif model.startswith("azure"):
        
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

    elif model.startswith("claude"):
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
            "model": model,
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

    elif model.startswith("mistral"):
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
        logger.info("Generating content with Mistral model: %s", model)

        flag = 0
        while True:
            try:
                if flag > 20: break
                response = client.chat.completions.create(
                    messages=mistral_messages,
                    model=model,
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

    elif model.startswith("THUDM"):
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
            "model": model,
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

    elif model.startswith("gemini"):
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
        if model == "gemini-pro-vision":
            message_history_str = ""
            for message in gemini_messages:
                message_history_str += "<|" + message['role'] + "|>\n" + message['parts'][0] + "\n"
            gemini_messages = [{"role": "user", "parts": [message_history_str, gemini_messages[-1]['parts'][1]]}]
            # gemini_messages[-1]['parts'][1].save("output.png", "PNG")

        # print(gemini_messages)
        api_key = os.environ.get("GENAI_API_KEY")
        assert api_key is not None, "Please set the GENAI_API_KEY environment variable"
        genai.configure(api_key=api_key)
        logger.info("Generating content with Gemini model: %s", model)
        request_options = {"timeout": 120}
        gemini_model = genai.GenerativeModel(model)
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
    elif model.startswith("qwen"):
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
        raise ValueError("Invalid model: " + model)
    