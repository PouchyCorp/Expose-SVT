from button import Button
import pygame as pg
from file_loader import load_image
from fonts import DIALOGUE_FONT_ITALIC

QCM_WINDOW = load_image('qcmwindow.png')

BUTTONS = [(load_image('buttonred.png'), (187, 592)), (load_image('buttonblue.png'), (1126, 592)), (load_image('buttongreen.png'), (187, 834)), (load_image('buttonyellow.png'), (1126, 834))]

def whiten(surface : 'pg.Surface'):
    """Whiten a surface to simulate a button press effect."""
    dest_surf = surface.copy()
    dest_surf.fill((60,60,60), special_flags=pg.BLEND_RGB_ADD)
    return dest_surf

class QCM:
    def __init__(self, question, options, correct_answer_ind):
        self.question_surface = DIALOGUE_FONT_ITALIC.render(question, True, (200-50, 147-50, 42))
        self.options = options
        self.correct_answer_ind = correct_answer_ind

        self.buttons : list[Button] = []
        for i, option in enumerate(self.options):
            button = Button(
                label=option,
                coord=BUTTONS[i][1],  # Adjust the y-coordinate for each button
                effect=self.check_answer,
                surf_active=whiten(BUTTONS[i][0]),
                surf_inactive=BUTTONS[i][0],
                param=[i]
            )
            self.buttons.append(button)

    def check_answer(self, answer):
        return answer == self.correct_answer_ind

    def handle_event(self, event):
        # Handle button events
        for button in self.buttons:
            if button.handle_event(event):
                if button.effect(*button.param):
                    return True
                    #TODO : Add feedback for correct/incorrect answer
        return False 
        #TODO : Add feedback for correct/incorrect answer

    def draw(self, screen : pg.Surface):
        # Display the question and options on the screen
        question_rect = self.question_surface.get_rect(center=(937, 415))

        screen.blit(QCM_WINDOW, (0, 0))
        screen.blit(self.question_surface, question_rect.topleft)
        mouse_pos = pg.mouse.get_pos()
        for button in self.buttons:
            button.draw(screen, button.rect.collidepoint(mouse_pos))  # Draw the button on the screen