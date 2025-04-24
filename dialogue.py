import pygame as pg
from fonts import DIALOGUE_FONT
from file_loader import load_image

MAX_LINE_SIZE = 40  # Maximum number of characters per line
PAGE_SIZE = 5  # Number of lines per page

class Dialogue:
    def __init__(self, text: list[str], character = None, documents = []):
        """
        Initialize a Dialogue instance.

        text: List of dialogue lines.
        """
        self.textes = text  # List of dialogue lines
        self.bliting_list: list[pg.Surface] = []  # List of surfaces to be blitted
        self.part_ind = 0  # Index of the current part of the dialogue
        self.current_dialogue_part = self.textes[self.part_ind]  # Current text to be shown
        self.page = 0  # Current page of the dialogue
        self.char_count = 0  # characters amount to be shown
        self.segmented_text = [''] * (len(self.current_dialogue_part) // MAX_LINE_SIZE + 1)  # Segmented text for the dialogue
        self.character_name = character  # Character associated with the dialogue\

        match self.character_name:
            case 'Jouvelot':
                self.character_sprite = load_image("placeholdercharacter.png")
            case _:
                self.character_sprite = pg.Surface((0, 0), pg.SRCALPHA)  # Default to a transparent surface if character not found
        
        self.documents = self.init_documents(documents)  # Initialize documents

    def init_documents(self, documents):
        """
        Initialize the documents for the dialogue.
        """
        document_sprites = []
        for doc in documents:
            document_sprites.append((load_image(doc['link']), doc['name']))  # Load each document and its name
        return document_sprites

    def get_text_surf(self, txt):
        """
        Get the surface for the current text.
        """
        return DIALOGUE_FONT.render(txt, False, 'green')

    def update(self):
        """
        Update the dialogue animation.
        """
        if self.char_count < len(self.current_dialogue_part): ## If there are remaining characters to be shown
            self.segmented_text[self.char_count // MAX_LINE_SIZE] += self.current_dialogue_part[self.char_count]
            self.char_count += 1  # Increment the character count

        
        self.bliting_list = []  # Reset bliting list
        for segment in self.segmented_text:
            self.bliting_list.append(self.get_text_surf(segment))

    def is_on_last_part(self):
        """
        Check if the dialogue is on the last part.
        """
        return True if self.part_ind == len(self.textes) - 1 else False
    
    def is_finished(self):
        """
        Check if the dialogue is finished.
        """
        return True if self.is_on_last_part() and self.char_count >= len(self.current_dialogue_part) else False

    def skip_to_next_part(self):
        """
        Skip to the next part of the dialogue.
        """
        if not self.is_on_last_part() and self.char_count >= len(self.current_dialogue_part):  # If not on the last part and all characters are shown
            self.part_ind += 1
            self.current_dialogue_part = self.textes[self.part_ind] # Change the text to be shown
            self.char_count = 0
            self.segmented_text = [''] * (len(self.current_dialogue_part) // MAX_LINE_SIZE + 1)


    def reset(self):
        """
        Reset the dialogue to the beginning.
        """
        self.anim_chars = ""
        self.current_dialogue_part = self.textes[0]
        self.bliting_list = []
        self.part_ind = 0
    
    def draw(self, screen: pg.Surface):
        """
        Draw the dialogue and bot animation on the screen.
        """
        screen.blit(pg.Surface((0,0), pg.SRCALPHA), (300 + 46 * 6, 750))  # Draw the background TODO: Replace with actual background image

        for i, surf in enumerate(self.bliting_list[-5:]):
            line_height = 812 + 27 * i  # Calculate the line height
            screen.blit(surf, (650, line_height))  # Draw each line of the dialogue
    
    def click_interaction(self) -> bool:
        """
        Handle click interaction and return True if the dialogue is finished.
        """
        if self.is_on_last_part():
            return True  # Dialogue is finished
        else:
            self.skip_to_next_part()  # Skip to the next part of the dialogue
            return False

    
