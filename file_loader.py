import json
import os

def load_json_file(filepath):
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"File not found: {filepath}")
    
    with open(filepath, 'r', encoding='utf-8') as file:
        try:
            return json.load(file)
        except json.JSONDecodeError as e:
            raise ValueError(f"Error decoding JSON from file: {filepath}") from e