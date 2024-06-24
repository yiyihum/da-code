import requests
import yaml
import json


class Airbyte_Evaluate:
    def __init__(self, input_connection_name, source_name, destination_name):
        with open("./config/airbyte.yml", 'r') as yaml_file:
            airbyte_config = yaml.safe_load(yaml_file)
        self.key = airbyte_config['key']
        self.input_connection_name = input_connection_name
        self.source_name = source_name
        self.destination_name = destination_name

    def set_input_connection_name(self, name):
        self.input_connection_name = name
    
    def list_connections(self):
        url = "https://api.airbyte.com/v1/connections?includeDeleted=false&limit=20&offset=0"

        headers = {
            "accept": "application/json",
            "authorization": f"Bearer {self.key}"
        }

        response = requests.get(url, headers=headers)

        self.connections = json.loads(response.text)
        return self.connections
    
    def list_sources(self):
        url = "https://api.airbyte.com/v1/sources?includeDeleted=false&limit=20&offset=0"

        headers = {
            "accept": "application/json",
            "authorization": f"Bearer {self.key}"
        }
        
        response = requests.get(url, headers=headers)
        self.sources = json.loads(response.text)
        return self.sources
    
    def list_destinations(self):
        url = "https://api.airbyte.com/v1/destinations?includeDeleted=false&limit=20&offset=0"

        headers = {
            "accept": "application/json",
            "authorization": f"Bearer {self.key}"
        }
        response = requests.get(url, headers=headers)
        self.destinations = json.loads(response.text)
        return self.destinations

    def is_succeed(self):
        connections = self.list_connections()
        if 'data' not in connections.keys():
            return 0
        connections = connections['data']
        
        find_connection = None
        flag = -1
        for i, item in enumerate(connections):
            if item['name'] == self.input_connection_name:
                flag = i; break
        find_connection = connections[i]
        source_id = find_connection['sourceId']
        destination_id = find_connection['destinationId']
        if flag != -1:
            return 1
        else:
            return 0
        