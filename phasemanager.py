import json
from file_loader import load_json_file

class PhaseManager:
    def __init__(self, phases_file, dialogues_file, minigame_configs, screen):
        self.phases = load_json_file(phases_file)
        self.dialogues = load_json_file(dialogues_file)
        self.minigame_configs = load_json_file(minigame_configs)
        self.screen = screen
        self.current_phase_index = 0

    def start_phase(self):
        if self.current_phase_index >= len(self.phases):
            print("All phases completed.")
            return False  # No more phases to process

        phase = self.phases[self.current_phase_index]
        phase_type = phase["type"]

        if phase_type == "dialogue":
            self.handle_dialogue(phase["link"])
        elif phase_type == "minigame":
            self.handle_minigame(phase["link"])
        elif phase_type == "transition":
            self.handle_transition(phase["link"])
        else:
            print(f"Unknown phase type: {phase_type}")

        self.current_phase_index += 1
        return phase_type  # Phase processed successfully

    def handle_dialogue(self, dialogue_id):
        dialogue = self.dialogues.get(dialogue_id, [])
        for line in dialogue:
            print(f"Dialogue: {line}")  # Replace with actual rendering logic

    def handle_minigame(self, minigame_id):
        minigame_config = next((m for m in self.minigame_configs if m["id"] == minigame_id), None)
        if minigame_config:
            print(f"Starting minigame: {minigame_config['title']}")  # Replace with actual minigame logic
        else:
            print(f"Minigame config not found: {minigame_id}")

    def handle_transition(self, transition_id):
        print(f"Transition: {transition_id}")  # Replace with actual transition logic
