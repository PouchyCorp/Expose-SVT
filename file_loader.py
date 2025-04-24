import json
import os
from pygame import error, image

def load_json_file(filepath):
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"File not found: {filepath}")
    
    with open(filepath, 'r', encoding='utf-8') as file:
        try:
            return json.load(file)
        except json.JSONDecodeError as e:
            raise ValueError(f"Error decoding JSON from file: {filepath}") from e
        
def load_image(filepath):
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Image file not found: {filepath}")
    
    try:
        return image.load(filepath).convert_alpha()
    except error as e:
        raise ValueError(f"Error loading image from file: {filepath}") from e
