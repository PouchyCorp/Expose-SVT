import pygame as pg
from phasemanager import PhaseManager


class Game:
    def __init__(self, screen):
        self.screen = screen
        self.state = 'start'
        self.phase_manager = PhaseManager(
            phases_file="phases.json",
            dialogues_file="dialogues.json",
            minigame_configs="minigameconfig.json",
            screen=screen
        )
    
    def update(self):
        """handles animations and updates the game state"""
    
    def draw(self):
        """draws the game elements on the screen"""
    
    def handle_click(self):
        """handles user input"""
        match self.state:
            case 'start':
                self.state = 'phase1'
            case 'minigame':
                '''handle minigame interaction'''
            case 'transition':
                '''handle transition interaction'''
                self.state = self.phase_manager.start_phase()
            case 'dialogue':
                self.state = 'minigame'
            case 'end':
                self.state = 'start'

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
            pg.time.wait(1000)  # Simulate phase duration

if __name__ == "__main__":
    pg.init()
    screen = pg.display.set_mode((800, 600))
    game = Game(screen)
    game.run()
    pg.quit()

