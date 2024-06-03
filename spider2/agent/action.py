#coding=utf8
import re
from dataclasses import dataclass, field
from typing import Optional, Any, Union, List, Dict
from abc import ABC

def remove_quote(text: str) -> str:
    """ 
    If the text is wrapped by a pair of quote symbols, remove them.
    In the middle of the text, the same quote symbol should remove the '/' escape character.
    """
    for quote in ['"', "'", "`"]:
        if text.startswith(quote) and text.endswith(quote):
            text = text[1:-1]
            text = text.replace(f"\\{quote}", quote)
            break
    return text.strip()


@dataclass
class Action(ABC):
    
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
class ExecuteBash(Action):

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
## ExecuteBash
Signature: ExecuteBash(code="shell_command")
Description: This action string will execute a valid shell command in the `code` field.
Example: ExecuteBash(code="ls -l")
"""

    @classmethod
    def parse_action_from_text(cls, text: str) -> Optional[Action]:
        matches = re.findall(r'ExecuteBash\(code=(.*)\)', text, flags=re.DOTALL)
        if matches:
            code = matches[-1]
            return cls(code=remove_quote(code))
        return None
    
    def __repr__(self) -> str:
        return f'{self.__class__.__name__}(code="{self.code}")'


@dataclass
class ExecuteSimplePython(Action):

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
        return f"ExecuteSimplePython:\n```\n{self.code.strip()}\n```"

    @classmethod
    def get_action_description(cls) -> str:
        return """
## ExecuteSimplePython
Signature: `ExecuteSimplePython`
```
executable_python_code
```

Description: This action executes a very simple Python command or snippet wrapped in paired ``` symbols. It is intended for short, exploratory code snippets. For longer or more complex code, please use CreateFile to write the code to a file and then execute it.

Example: ExecuteSimplePython:
```
print("Hello, world!")
```
"""

    @classmethod
    def parse_action_from_text(cls, text: str) -> Optional[Action]:
        matches = re.findall(r'ExecuteSimplePython.*?```[ \t]*(\w+)?[ \t]*\r?\n(.*)[\r\n \t]*```', text, flags=re.DOTALL)
        if matches:
            code = matches[-1][1]
            return cls(code=code.strip())
        return None
    
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}\n '''\n{self.code}\n'''"


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
## CreateFile
Signature: CreateFile(filepath="path/to/file"):
```
file_content
```
Description: This action will create a file in the field `filepath` with the content wrapped by paired ``` symbols. Make sure the file content is complete and correct. If the file already exists, you can only use EditFile to modify it.
Example: CreateFile(filepath="hello_world.py"):
```
print("Hello, world!")
```
"""

    @classmethod
    def parse_action_from_text(cls, text: str) -> Optional[Action]:
        matches = re.findall(r'CreateFile\(filepath=(.*?)\).*?```[ \t]*(\w+)?[ \t]*\r?\n(.*)[\r\n \t]*```', text, flags=re.DOTALL)
        if matches:
            filepath = matches[-1][0].strip()
            code = matches[-1][2].strip()
            return cls(code=code, filepath=remove_quote(filepath))
        return None
    
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(filepath='{self.filepath}':\n'''\n{self.code}\n''')"
       
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
## EditFile
Signature: EditFile(filepath="path/to/file"):
```
file_content
```
Description: This action will overwrite the file specified in the filepath field with the content wrapped in paired ``` symbols. Normally, you need to read the file before deciding to use EditFile to modify it.
Example: EditFile(filepath="hello_world.py"):
```
print("Hello, world!")
```
"""

    @classmethod
    def parse_action_from_text(cls, text: str) -> Optional[Action]:
        matches = re.findall(r'EditFile\(filepath=(.*?)\).*?```[ \t]*(\w+)?[ \t]*\r?\n(.*)[\r\n \t]*```', text, flags=re.DOTALL)
        if matches:
            filepath = matches[-1][0].strip()
            code = matches[-1][2].strip()
            return cls(code=code, filepath=remove_quote(filepath))
        return None

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

    code : str = field(
        default=''
    )

    @classmethod
    def get_action_description(cls) -> str:
        return """
## Terminate
Signature: Terminate(output="literal_answer_or_output_path")
Description: This action denotes the completion of the entire task and returns the final answer or the output file/folder path. Make sure the output file is located in the initial workspace directory.
Example1: Terminate(output="New York")
Example2: Terminate(output="result.txt")
Example3: Terminate(output="FAIL")

"""

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}(output="{self.output}")'

    @classmethod
    def parse_action_from_text(cls, text: str) -> Optional[Action]:
        matches = re.findall(r'Terminate\(output=(.*)\)', text, flags=re.DOTALL)
        if matches:
            output = matches[-1]
            return cls(output=remove_quote(output))
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