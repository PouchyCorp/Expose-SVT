import sys, os


if hasattr(sys, '_MEIPASS'):
    # If the script is running as a bundled executable, change the working directory to the location of the executable
    # This is necessary for loading resources correctly in a bundled application
    # os.chdir(sys._MEIPASS) if hasattr(sys, '_MEIPASS') else None
    os.chdir(sys._MEIPASS) 


def transition(screen : 'pg.Surface', current_frame : 'pg.Surface', next_frame : 'pg.Surface', time : float = 2):
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
    def __init__(self, screen : 'pg.Surface'):
        """Initialize the game"""
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

        img = load_image('buttonred.png')
        self.start_button = Button('Commencer', (screen.get_width() // 2 - img.get_width()//2, screen.get_height() // 2 + 200 - img.get_height()//2), int, whiten(img), img)
        
        self.title_surf = load_image('title.png')
        self.title_rect = self.title_surf.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 - 200))

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
        next_text_surf = DESCRIPTION_FONT.render("Cliquez pour continuer", True, (255, 255, 255))
        next_text_rect = next_text_surf.get_rect(bottomright=(self.screen.get_width() - 20, self.screen.get_height() - 20))
        match self.state:
            case 'start':
                '''draw start elements'''
                self.screen.blit(TITLE_BACKGROUND, (0, 0))
                self.screen.blit(self.title_surf, self.title_rect.topleft)
                self.start_button.draw(self.screen, self.start_button.rect.collidepoint(mouse_pos))
            case 'minigame':
                '''draw minigame elements'''
                self.minigame.draw(self.screen)
            case 'transition':
                '''draw transition elements'''
                # draw transition text if any
                if self.transition_text:
                    text_surf = BIG_FONT.render(self.transition_text, True, (255, 255, 255))
                    text_rect = text_surf.get_rect(center=(self.screen.get_width() // 2, 200))
                    self.screen.blit(text_surf, text_rect)
                self.screen.blit(next_text_surf, next_text_rect)
            case 'dialogue':
                self.dialogue.draw(self.screen)
                if self.dialogue.char_count >= len(self.dialogue.current_dialogue_part):
                    self.screen.blit(next_text_surf, next_text_rect)
                


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
                    CLICK_SOUND.play()
                    self.handle_click(event)
                
            
            self.update()
            self.draw()

            pg.display.flip()



if __name__ == "__main__":
    import pygame as pg

    pg.init()
    pg.mixer.init()

    screen = pg.display.set_mode((1920,1080))
    
    from phasemanager import PhaseManager
    from math import pi, sin
    from qcm import QCM, whiten
    from button import Button
    from dialogue import Dialogue
    from fonts import DESCRIPTION_FONT, BIG_FONT
    from file_loader import load_image, load_and_resize_image

    MUSIC = pg.mixer.Sound('assets/music.wav')
    MUSIC.set_volume(0.1)
    MUSIC.play(-1)  # Play the music in a loop
    
    CLICK_SOUND = pg.mixer.Sound('assets/clic.mp3')
    CLICK_SOUND.set_volume(0.5)

    TITLE_BACKGROUND = load_and_resize_image('titlebackground.jpg')

    while True:
        game = Game(screen)
        game.run()

