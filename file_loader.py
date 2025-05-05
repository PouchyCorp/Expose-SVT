import json
import os
from pygame import error, image, transform

folder = 'assets/'

def load_json_file(filepath):
    if not os.path.exists(folder+filepath):
        raise FileNotFoundError(f"File not found: {filepath}")
    
    with open(folder+filepath, 'r', encoding='utf-8') as file:
        try:
            return json.load(file)
        except json.JSONDecodeError as e:
            raise ValueError(f"Error decoding JSON from file: {filepath}") from e
        
def load_image(filepath):
    if not os.path.exists(folder+filepath):
        raise FileNotFoundError(f"Image file not found: {filepath}")
    
    return image.load(folder+filepath).convert_alpha()

def load_and_resize_image(filepath):
    image = load_image(filepath)
    return transform.scale_by(image, 0.4)