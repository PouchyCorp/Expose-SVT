from button import Button
import pygame as pg
from file_loader import load_image
from fonts import BIG_FONT
WRONG_SOUND = pg.mixer.Sound('assets/wrong-answer-buzzer.mp3')
CORRECT_SOUND = pg.mixer.Sound('assets/correct.mp3')

QCM_WINDOW = load_image('qcmwindow.png')

BUTTONS = [(load_image('buttonred.png'), (187, 592)), (load_image('buttonblue.png'), (1126, 592)), (load_image('buttongreen.png'), (187, 834)), (load_image('buttonyellow.png'), (1126, 834))]

def whiten(surface : 'pg.Surface'):
    """Whiten a surface to simulate a button press effect."""
    dest_surf = surface.copy()
    dest_surf.fill((60,60,60), special_flags=pg.BLEND_RGB_ADD)
    return dest_surf

class QCM:
    def __init__(self, question, options, correct_answer_ind):
        self.question_surface = self.render_multiline_text(question, BIG_FONT, 1800, (144,213,255))  # Adjust width as needed
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

    @staticmethod
    def render_multiline_text(text, font, max_width, color):
        """Render text into multiple lines if it exceeds max_width."""
        words = text.split(' ')
        lines = []
        current_line = []

        for word in words:
            test_line = ' '.join(current_line + [word])
            if font.size(test_line)[0] <= max_width:
                current_line.append(word)
            else:
                lines.append(' '.join(current_line))
                current_line = [word]

        if current_line:
            lines.append(' '.join(current_line))

        surfaces = [font.render(line, True, color) for line in lines]
        total_height = sum(surf.get_height() for surf in surfaces)
        combined_surface = pg.Surface((max_width, total_height), pg.SRCALPHA)

        y_offset = 0
        for surf in surfaces: 
            combined_surface.blit(surf, (0, y_offset))
            y_offset += surf.get_height()

        return combined_surface

    def check_answer(self, answer):
        return answer == self.correct_answer_ind

    def handle_event(self, event):
        # Handle button events
        for button in self.buttons:
            if button.handle_event(event):
                if button.effect(*button.param):
                    pg.mixer.Sound.play(CORRECT_SOUND)
                    return True
        pg.mixer.Sound.play(WRONG_SOUND)
        return False 
    
    def draw(self, screen : pg.Surface):
        # Display the question and options on the screen
        question_rect = self.question_surface.get_rect(center=(937, 415))

        screen.blit(QCM_WINDOW, (0, 0))
        screen.blit(self.question_surface, question_rect.topleft)
        mouse_pos = pg.mouse.get_pos()
        for button in self.buttons:
            button.draw(screen, button.rect.collidepoint(mouse_pos))  # Draw the button on the screen