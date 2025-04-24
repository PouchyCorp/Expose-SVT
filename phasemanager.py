from file_loader import load_json_file, load_image
from pygame import Surface, SRCALPHA

class PhaseManager:
    def __init__(self, phases_file, dialogues_file, minigame_configs, screen, init_new_phase):
        self.phases = load_json_file(phases_file)
        self.dialogues = load_json_file(dialogues_file)
        self.minigame_configs = load_json_file(minigame_configs)
        self.screen = screen
        self.current_phase_index = 0
        self.init_new_phase = init_new_phase
        self.current_phase = self.phases[self.current_phase_index]

    def start_phase(self):
        if self.current_phase_index >= len(self.phases):
            return False  # No more phases to process

        self.current_phase_index += 1

        self.current_phase = self.phases[self.current_phase_index]

        match self.current_phase['type']:
            case 'dialogue':
                dialogue_info = {
                    'type': 'dialogue',
                    'dialogue': self.dialogues[self.current_phase['link']],
                    'background': load_image(self.current_phase['background']),
                    'character': self.current_phase.get('character', None),
                    'documents': self.current_phase.get('documents', []),
                }
                self.init_new_phase(dialogue_info)

            case 'minigame':
                minigame_info = {
                    'type': 'minigame',
                    'minigame': self.minigame_configs[self.current_phase['link']],
                    'background': load_image(self.current_phase['background']),
                }
                self.init_new_phase(minigame_info)
            
            case 'transition':
                transition_info = {
                    'type': 'transition',
                    'background': load_image(self.current_phase['background']),
                    'text'  : self.current_phase.get('text', ''),
                }
                self.init_new_phase(transition_info)

        return load_image(self.current_phase['background'])  # Phase processed successfully
