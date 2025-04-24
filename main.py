import pygame as pg
from phasemanager import PhaseManager
from math import pi, sin

from dialogue import Dialogue

def transition(screen : pg.Surface, current_frame : pg.Surface, next_frame : pg.Surface, time : float = 2):
        """Simple fade-in-out transition between one frame to another, can be easily used at other places.  
        Reimplementation of the __play_transition method above"""
        clock = pg.time.Clock()
        mask = pg.Surface((screen.get_width(), screen.get_height()))
        mask.fill((0, 0, 0))
        incr = 0
        step_count = time * 60  # Number of steps for the transition

        while incr < pi:
            clock.tick(60)
            incr += pi / step_count  # Increment the angle for the sine function

            if incr < pi / 2:
                # First half of the transition: draw the current cutscene and dialogue
                screen.blit(current_frame, (0,0))
            else:
                # Second half of the transition: draw the normal game background
                screen.blit(next_frame, (0,0))

            # Use the sine function to create a smooth fade out effect
            # sin(incr) varies from 0 to 1 as incr goes from 0 to pi/2, and from 1 to 0 as incr goes from pi/2 to pi
            mask.set_alpha(sin(incr) * 255)
            screen.blit(mask, (0, 0))
            pg.display.flip()
        
        return next_frame

class Game:
    def __init__(self, screen):
        self.screen : pg.Surface = screen 
        self.state = 'start'
        self.phase_manager = PhaseManager(
            phases_file="phases.json",
            dialogues_file="dialogues.json",
            minigame_configs="minigameconfig.json",
            screen=screen,
            init_new_phase= self.init_new_phase)
    
    def update(self):
        """handles animations and updates the game state"""
        match self.state:
            case 'minigame':
                '''handle minigame animation'''
            case 'dialogue':
                self.dialogue.update()
    
    def draw(self):
        """draws the game elements on the screen"""
        self.screen.blit(self.background, (0, 0))
        match self.state:
            case 'minigame':
                '''draw minigame elements'''
            case 'transition':
                '''draw transition elements'''
                # draw transition text if any
            case 'dialogue':
                self.dialogue.draw(self.screen)
                

    
    def handle_click(self):
        """handles user input"""
        match self.state:
            case 'start':
                transition(self.screen, self.background, self.phase_manager.start_phase())
            case 'minigame':
                '''handle minigame interaction'''
            case 'transition':
                '''handle transition interaction'''
            case 'dialogue':
                self.dialogue.click_interaction()
                if self.dialogue.is_on_last_part():
                    transition(self.screen, self.background, self.phase_manager.start_phase())
                
            case 'end':
                self.phase_manager.current_phase_index = 0
                self.state = 'start'
                transition(self.screen, self.background, pg.Surface((1920, 1080)), time=4)
    
    def init_new_phase(self, phase_info):
        match phase_info['type']:
            case 'minigame':
                self.state = 'minigame'
                self.background = phase_info['background']
                # Initialize minigame with phase_info
            case 'transition':
                self.state = 'transition'
                self.background = phase_info['background']
                self.transition_text = phase_info['text']
                # Initialize transition with phase_info
            case 'dialogue':
                self.state = 'dialogue'
                self.dialogue = Dialogue(phase_info['dialogue'], phase_info['character'], phase_info['documents'])
                self.background = phase_info['background']
                # Initialize dialogue with phase_info
            case _:
                raise ValueError(f"Unknown phase type: {phase_info['type']}")

    def run(self):
        running = True
        while running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False

            
            self.screen.fill("black")
            if not self.phase_manager.start_phase():
                running = False  # Exit loop when all phases are completed

            pg.display.flip()



if __name__ == "__main__":
    pg.init()
    screen = pg.display.set_mode((800, 600))
    game = Game(screen)
    game.run()
    pg.quit()

