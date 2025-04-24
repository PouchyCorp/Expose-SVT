from button import Button
import pygame as pg

class QCM:
    def __init__(self, question, options, correct_answer_ind):
        self.question_surface = pg.font.Font(None, 36).render(question, True, (255, 255, 255))
        self.options = options
        self.correct_answer_ind = correct_answer_ind

        self.buttons : list[Button] = []
        for i, option in enumerate(self.options):
            button = Button(
                label=option,
                coord=(100, 100 + i * 100),  # Adjust the y-coordinate for each button
                effect=self.check_answer,
                surf_active=pg.Surface((200, 50)),
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

    def draw(self, screen):
        # Display the question and options on the screen
        question_rect = self.question_surface.get_rect(center=(960, 540))
        screen.blit(self.question_surface, question_rect.topleft)

        mouse_pos = pg.mouse.get_pos()
        for button in self.buttons:
            button.draw(screen, button.rect.collidepoint(mouse_pos))  # Draw the button on the screen