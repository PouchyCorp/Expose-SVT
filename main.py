import sys, os

if hasattr(sys, '_MEIPASS'):
    # If the script is running as a bundled executable, change the working directory to the location of the executable
    # This is necessary for loading resources correctly in a bundled application
    # os.chdir(sys._MEIPASS) if hasattr(sys, '_MEIPASS') else None
    os.chdir(sys._MEIPASS) 

import pygame as pg
from phasemanager import PhaseManager
from math import pi, sin
from qcm import QCM
from button import Button
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
        self.background = pg.Surface((screen.get_width(), screen.get_height()))
        self.phase_manager = PhaseManager(
            phases_file="phases.json",
            dialogues_file="dialogues.json",
            minigame_configs="minigameconfig.json",
            screen=screen,
            init_new_phase= self.init_new_phase)
        self.game_over = False

        self.start_button = Button('Commencer', (screen.get_width() // 2, screen.get_height() // 2), int, pg.Surface((200, 50)))
    
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
        mouse_pos = pg.mouse.get_pos()
        match self.state:
            case 'start':
                '''draw start elements'''
                self.start_button.draw(self.screen, self.start_button.rect.collidepoint(mouse_pos))
            case 'minigame':
                '''draw minigame elements'''
                self.minigame.draw(self.screen)
            case 'transition':
                '''draw transition elements'''
                # draw transition text if any
            case 'dialogue':
                self.dialogue.draw(self.screen)
                


    def handle_click(self, event):
        """handles user input"""
        match self.state:
            case 'start':
                if self.start_button.handle_event(event):
                    transition(self.screen, self.background, self.phase_manager.start_phase())
            case 'minigame':
                '''handle minigame interaction'''
                if self.minigame.handle_event(event):
                    transition(self.screen, self.background, self.phase_manager.start_phase(), 0.5)
            case 'transition':
                '''handle transition interaction'''
                transition(self.screen, self.background, self.phase_manager.start_phase())
            case 'dialogue':
                self.dialogue.click_interaction()
                if self.dialogue.is_finished():
                    transition(self.screen, self.background, self.phase_manager.start_phase(), 1)
                    self.dialogue.reset()
            case 'end':
                transition(self.screen, self.background, pg.Surface((1920, 1080)), time=4)
                self.game_over = True
    
    def init_new_phase(self, phase_info):
        match phase_info['type']:
            case 'minigame':
                self.state = 'minigame'
                self.background = phase_info['background']
                self.minigame = QCM(phase_info['minigame']['question'], phase_info['minigame']['options'], phase_info['minigame']['correct_answer_ind'])
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
            case 'end':
                print('end')
                self.state = 'end'
                self.background = phase_info['background']
                # Initialize end phase with phase_info
            case _:
                raise ValueError(f"Unknown phase type: {phase_info['type']}")

    def run(self):
        clock = pg.time.Clock()
        while not self.game_over:
            clock.tick(60)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    from sys import exit
                    exit()

                if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                    self.handle_click(event)
                
                if event.type == pg.KEYDOWN and event.key == pg.K_d:
                    print(str(pg.mouse.get_pos()))
            
            self.update()
            self.draw()

            font  = pg.font.SysFont('Arial', 30)
            screen.blit(font.render(str(pg.mouse.get_pos()), True, (255, 255, 255)), (0,0))

            pg.display.flip()



if __name__ == "__main__":
    pg.init()
    screen = pg.display.set_mode((1920,1080))
    while True:
        game = Game(screen)
        game.run()

