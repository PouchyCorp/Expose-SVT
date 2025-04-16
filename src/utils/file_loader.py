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

def load_dialogue_file(filename):
    return load_json_file(os.path.join('assets', 'dialogues', filename))

def load_phase_file(filename):
    return load_json_file(os.path.join('assets', 'phases', filename))

def load_minigame_file(filename):
    return load_json_file(os.path.join('assets', 'minigames', filename))