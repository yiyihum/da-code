#coding=utf8
import re
from dataclasses import dataclass, field
from typing import Optional, Any, Union, List, Dict


def remove_quote(text: str) -> str:
    """ Remove the quote symbols from the text. """
    text = text.replace(r'\\"', '"').replace(r"\\'", "'")
    for quote in ['"', "'", '`']:
        if text.startswith(quote):
            text = text[1:]
            if text.endswith(quote):
                text = text[:-1]
            break
    return text.strip()


@dataclass
class Action():
    
    action_type: str = field(
        repr=False,
        metadata={"help": 'type of action, e.g. "exec_code", "create_file", "terminate"'}
    )

    @classmethod
    def get_action_description(cls) -> str:
        return """
Action: action format
Description: detailed definition of this action type.
Usage: example cases
Observation: the observation space of this action type.
"""

    @classmethod
    def parse_action_from_text(cls, text: str) -> Optional[Any]:
        raise NotImplementedError



@dataclass
class ExecuteCode(Action):

    action_type: str = field(
        default="exec_code",
        init=False,
        repr=False,
        metadata={"help": 'type of action, c.f., "exec_code"'}
    )

    code: str = field(
        metadata={"help": 'command to execute'}
    )

    @classmethod
    def get_action_description(cls) -> str:
        return """
Action: ExecuteCode(code=\"shell_command\")
Description: This action string will execute a valid shell command in the `code` field, such as `cat path/to/file.txt` and `python path/to/file.py`. Please pay attention to the current working directory. If you execute a `cd new_path` command, the working directory will be changed. If no further action is taken, the working directory will still be the changed new_path. Furthermore, for two special commands `cd new_path` and `export var=val`, they must occur as a single command and cannot use `&&` or `;` to chain together. If you want to, for example, set multiple environment variables, please use multiple ExecuteCode actions.
Usage: ExecuteCode(code="ls -l")
Observation: The observation space is the stdout or stderr of the executed command in the bash terminal.
"""

    @classmethod
    def parse_action_from_text(cls, text: str) -> Optional[Action]:
        matches = re.findall(r'ExecuteCode\(code=(.*)\)', text, flags=re.DOTALL)
        if matches:
            code = matches[-1]
            return cls(code=remove_quote(code))
        return None

# @dataclass
# class PackageInstall(Action):

#     action_type: str = field(
#         default="package_install",
#         init=False,
#         repr=False,
#         metadata={"help": 'type of action, c.f., "package_install"'}
#     )

#     package: str = field(
#         metadata={"help": 'package to install'}
#     )

#     @classmethod
#     def get_action_description(cls) -> str:
#         return """
# Action: PackageInstall(package=\"package_name\")
# Description: This action string will install a python package in the `package` field for the environment. Notice that, you can only install a package that is available via the pip command. You can also specify the version of the package to install, such as package="numpy==1.19.5". If you want to install multiple packages, use whitespaces to separate them, such as package="numpy pandas".
# Usage: PackageInstall(package="sklearn")
# Observation: The observation space is a text message indicating whether this action is executed successfully or not.
# """

#     @classmethod
#     def parse_action_from_text(cls, text: str) -> Optional[Action]:
#         matches = re.findall(r'PackageInstall\(package=(.*?)\)', text, flags=re.DOTALL)
#         if matches:
#             package = matches[-1]
#             return cls(package=remove_quote(package))
#         return None


@dataclass
class PythonSnippet(Action):

    action_type: str = field(
        default="python_snippet",
        init=False,
        repr=False,
        metadata={"help": 'type of action, c.f., "python_snippet"'}
    )

    code: str = field(
        metadata={"help": 'executable python commands or snippets'}
    )

    def __repr__(self) -> str:
        return f"PythonSnippet:\n```\n{self.code.strip()}\n```"

    @classmethod
    def get_action_description(cls) -> str:
        return """
Action: PythonSnippet:
```
executable_python_code
```
Description: This action string will execute a valid python command or snippet wrapped by paired ``` symbols. If the code snippet contains multiple lines, pay attention to the indentation. And if you want to know the value of one variable, please use the print `function` explicitly. Notice that, the python code execution is continuous, which means that the variables, functions and classes defined in previous code snippets can be used in the following code snippet.
Usage: PythonSnippet:
```
class Foo():
    def __init__(self):
        print('hello world!')
        
Foo()
```
Observation: The observation space is the output or error message of the executed python code.
"""

    @classmethod
    def parse_action_from_text(cls, text: str) -> Optional[Action]:
        matches = re.findall(r'PythonSnippet.*?```[ \t]*(\w+)?[ \t]*\r?\n(.*)[\r\n \t]*```', text, flags=re.DOTALL)
        if matches:
            code = matches[-1][1]
            return cls(code=code.strip())
        return None


# @dataclass
# class SQLCommand(Action):

#     action_type: str = field(
#         default="sql_command",
#         init=False,
#         repr=False,
#         metadata={"help": 'type of action, c.f., "sql_command"'}
#     )

#     command: str = field(
#         metadata={"help": 'SQL command to execute'}
#     )

#     @classmethod
#     def get_action_description(cls) -> str:
#         return """
# Action: SQLCommand(command=\"sql_command\")
# Description: This action string will execute a valid SQL command in the `command` field, such as `SELECT * FROM table_name` and `INSERT INTO table_name VALUES (value1, value2, value3)`.
# Usage: SQLCommand(command="SELECT * FROM table_name")
# Observation: The observation space is the execution results or errors in the corresponding database server.
# """

#     @classmethod
#     def parse_action_from_text(cls, text: str) -> Optional[Action]:
#         matches = re.findall(r'SQLCommand\(command=(.*)\)', text, flags=re.DOTALL)
#         if matches:
#             command = matches[-1]
#             return cls(command=remove_quote(command))
#         return None


@dataclass
class CreateFile(Action):

    action_type: str = field(
        default="create_file",
        init=False,
        repr=False,
        metadata={"help": 'type of action, c.f., "create_file"'}
    )

    code: str = field(
        metadata={"help": 'code to write into file'}
    )

    filepath: Optional[str] = field(
        default=None,
        metadata={"help": 'name of file to create'}
    )

    def __repr__(self) -> str:
        return f"CreateFile(filepath=\"{self.filepath}\"):\n```\n{self.code.strip()}\n```"

    @classmethod
    def get_action_description(cls) -> str:
        return """
Action: CreateFile(filepath="path/to/file"):
```
file_content
```
Description: This action will create a file in the field `filepath` with the content wrapped by paired ``` symbols. Notice that, the file content can be free form text, arbitrary programming langugage codes or configurations. For more structured format (e.g., .csv or .json files), you can use the CreateFile action to firstly create a writing-to-file program file (e.g., .py or .sh) and then use the ExecuteCode action to execute the program and generate the structured file. Remember to provide the field `filepath` besides the "file_content" in this action even if the created file is only temporary and will be deleted later.
Usage: CreateFile(filepath="hello_world.py"):
```
print("Hello, world!")
```
Observation: The observation space is a text message indicating whether this action is executed successfully or not.
"""

    @classmethod
    def parse_action_from_text(cls, text: str) -> Optional[Action]:
        matches = re.findall(r'CreateFile\(filepath=(.*?)\).*?```[ \t]*(\w+)?[ \t]*\r?\n(.*)[\r\n \t]*```', text, flags=re.DOTALL)
        if matches:
            filepath = matches[-1][0].strip()
            code = matches[-1][2].strip()
            return cls(code=code, filepath=remove_quote(filepath))
        return None
    
    
    
    
    
    
    
@dataclass
class EditFile(Action):
    action_type: str = field(
        default="edit_file",
        init=False,
        repr=False,
        metadata={"help": 'type of action, c.f., "edit_file"'}
    )

    code: str = field(
        metadata={"help": 'code to write into file'}
    )

    filepath: Optional[str] = field(
        default=None,
        metadata={"help": 'name of file to edit'}
    )

    def __repr__(self) -> str:
        return f"EditFile(filepath=\"{self.filepath}\"):\n```\n{self.code.strip()}\n```"

    @classmethod
    def get_action_description(cls) -> str:
        return """
Action: EditFile(filepath="path/to/file"):
```
file_content
```
Description: This action will edit a file in the field `filepath` with the content wrapped by paired ``` symbols. Notice that, the file content can be free form text, arbitrary programming langugage codes or configurations. Normally, you need to read a file before deciding whether to use EditFile to modify it. You need to give the entire modified file content. 
Usage: EditFile(filepath="hello_world.py"):
```
print("Hello, world!")
```
Observation: The observation space is a text message indicating whether this action is executed successfully or not.
"""

    @classmethod
    def parse_action_from_text(cls, text: str) -> Optional[Action]:
        matches = re.findall(r'EditFile\(filepath=(.*?)\).*?```[ \t]*(\w+)?[ \t]*\r?\n(.*)[\r\n \t]*```', text, flags=re.DOTALL)
        if matches:
            filepath = matches[-1][0].strip()
            code = matches[-1][2].strip()
            return cls(code=code, filepath=remove_quote(filepath))
        return None


# @dataclass
# class WebSearch(Action):

#     action_type: str = field(
#         default="web_search",
#         init=False,
#         repr=False,
#         metadata={"help": 'type of action, c.f., "web_search"'}
#     )

#     link: Optional[str] = field(
#         default=None,
#         metadata={"help": 'link to the website'}
#     )

#     @classmethod
#     def get_action_description(cls):
#         return """
# Action: WebSearch(link=\"web_url\")
# Description: This action will fetch content from the web when you need extra information to make decisions. You need to provide the `link` field which is an accessible website. The fetched content is a preprocessed HTML page by removing function tags (e.g., script, style) and extracting useful tags (e.g., p, li, div, span). The extracted content is then concatenated into a single string. If the preprocessed string is too long, it will be truncated.
# Usage: WebSearch(link="https://en.wikipedia.org/wiki/Main_Page")
# Observation: The observation space is the preprocessed HTML page content.
# """

#     @classmethod
#     def parse_action_from_text(cls, text: str) -> Optional[Action]:
#         matches = re.findall(r'WebSearch\(link=(.*?)\)', text, flags=re.DOTALL)
#         if matches:
#             link = matches[-1]
#             return cls(link=remove_quote(link))
#         return None


@dataclass
class Terminate(Action):

    action_type: str = field(
        default="terminate",
        init=False,
        repr=False,
        metadata={"help": "terminate action representing the task is finished, or you think it is impossible for you to complete the task"}
    )

    output: Optional[str] = field(
        default=None,
        metadata={"help": "answer to the task or output file path or 'FAIL', if exists"}
    )

    @classmethod
    def get_action_description(cls) -> str:
        return """
Action: Terminate(output=\"literal_answer_or_output_path\")
Description: This action denotes the completion of the entire task and returns the final answer or the output file/folder path. If the output field is a directory or filepath, you can use the relative path of the current working directory or directly use the absolute path.
Usage1: Terminate(output="New York")
Usage2: Terminate(output="/workspace/result.txt")
Usage3: Terminate(output="FAIL")
Observation: The observation space is empty since the task is finished.
"""

    @classmethod
    def parse_action_from_text(cls, text: str) -> Optional[Action]:
        matches = re.findall(r'Terminate\(output=(.*)\)', text, flags=re.DOTALL)
        if matches:
            output = matches[-1]
            return cls(output=remove_quote(output))
        return None