import pygame as pg
from fonts import DIALOGUE_FONT, DIALOGUE_FONT_BOLD, DIALOGUE_FONT_ITALIC
from file_loader import load_and_resize_image, load_image
from random import choice

MAX_LINE_SIZE = 140  # Maximum number of characters per line
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
        self.parsed_dialogue_part = self.parse_text(self.current_dialogue_part)  # Parsed text to be shown
        self.page = 0  # Current page of the dialogue
        self.char_count = 0  # characters amount to be shown
        self.segmented_text = [''] * (len(self.current_dialogue_part) // MAX_LINE_SIZE + 1)  # Segmented text for the dialogue
        self.character_name = character  # Character associated with the dialogue\

        match self.character_name:
            case 'Jouvelot':
                self.sprites_choices = [load_and_resize_image("jouvelot1.png"), load_and_resize_image("jouvelot2.png"), load_and_resize_image("jouvelot3.png"), load_and_resize_image("jouvelot4.png"), load_and_resize_image("jouvelot5.png")]
            case 'Meteo':
                self.sprites_choices = [load_and_resize_image("riche1.png"), load_and_resize_image("riche2.png"), load_and_resize_image("riche3.png"), load_and_resize_image("riche4.png")]
            
            case 'Climato':
                self.sprites_choices = [load_and_resize_image("sdf1.png"), load_and_resize_image("sdf2.png"), load_and_resize_image("sdf3.png"), load_and_resize_image("sdf4.png")]
            
            case 'Villageois':
                self.sprites_choices = [load_and_resize_image("pnj1.png"), load_and_resize_image("pnj2.png")]

            case 'Pmurt':
                self.sprites_choices = [load_and_resize_image("trump1.png"), load_and_resize_image("trump2.png"), load_and_resize_image("trump3.png")]

            case _:
                self.sprites_choices = [pg.Surface((0, 0), pg.SRCALPHA)]
    
        self.character_sprite = choice(self.sprites_choices)
        
        self.documents = self.init_documents(documents)  # Initialize documents


    def crop_parsed_text(self, parse_text : list[list[str, int]], start : int, stop) -> list[list[str, int]]:
        """
        Crop the parsed text to fit the size.
        """
        cropped_text = []
        
        stop -= start  # Adjust stop to account for the starting position

        shortened_parse_text = []
        for segment in parse_text:
            if len(segment[0]) > start:
                shortened_parse_text.append([segment[0][start:], segment[1]])
                start = 0
            elif start > 0:
                start = start - len(segment[0])
            else:
                shortened_parse_text.append(segment)
        
        for segment in shortened_parse_text:
            if len(segment[0]) > stop:
                cropped_text.append([segment[0][:stop], segment[1]])
                break
            else:
                cropped_text.append(segment)
                stop -= len(segment[0])

        return cropped_text
            

    def init_documents(self, documents):
        """
        Initialize the documents for the dialogue.
        """
        document_sprites = []
        for doc in documents:
            document_sprites.append((load_image(doc['link']), doc['name']))  # Load each document and its name
        return document_sprites

    def get_text_surf(self, txt : list[list[str, int]]) -> pg.Surface:
        """
        Get the surface for the current text.
        """

        if len(txt) == 0:
            return pg.Surface((0, 0), pg.SRCALPHA)

        surf_list : list[pg.Surface]= []  # Create a transparent surface
        font_color = 'white'  # Default font color
        for segment, segment_type in txt:
            match segment_type:
                case 1:  # Bold text
                    surf_list.append(DIALOGUE_FONT_BOLD.render(segment, False, font_color))
                case 2:  # Italic text
                    surf_list.append(DIALOGUE_FONT_ITALIC.render(segment, False, font_color))
                case 3:  # Red text
                    surf_list.append(DIALOGUE_FONT.render(segment, False, 'red'))
                case 4:  # Blue text
                    surf_list.append(DIALOGUE_FONT.render(segment, False, 'blue'))
                case _: # Default to normal text
                    surf_list.append(DIALOGUE_FONT.render(segment, False, font_color))
        
        final_surf : pg.Surface = pg.Surface((sum([s.get_width() for s in surf_list]), 100), pg.SRCALPHA)  # Create a transparent surface
        x = 0
        for surf in surf_list:
            final_surf.blit(surf, (x, 0))
            x += surf.get_width()
        return final_surf

    def update(self):
        """
        Update the dialogue animation.
        """
        if self.char_count <= len(self.current_dialogue_part): ## If there are remaining characters to be shown
            self.segmented_text[self.char_count // MAX_LINE_SIZE] = self.crop_parsed_text(self.parsed_dialogue_part, (self.char_count // MAX_LINE_SIZE) * MAX_LINE_SIZE , self.char_count)
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
    
    def parse_text(self, text):
        parsed_text : list[list]= [['', 0]]  # List of tuples (text, status) 0: normal, 1: bold, 2: italic, 3: red, 4: blue 
        i = 0  # Index for the text
        while i < len(text):
            for sig, sig_ind in [('b', 1), ('i', 2), ('r', 3), ('b', 4)]:

                if i < len(text)-1 and text[i] == '/' and text[i+1] == sig:
                    i += 3  # Skip the esc characters ('/', sig, '/')
                    parsed_text.append(['', sig_ind])
                    while i < len(text)-1 and text[i] != '/':
                        parsed_text[-1][0] += text[i]
                        i += 1
                    i += 1  # Skip the '/' character
                    parsed_text.append(['', 0])
                    break
            
            if i > len(text):
                break
            parsed_text[-1][0] += text[i]
            i += 1
        parsed_text = [segment for segment in parsed_text if segment[0] != '']  # Remove empty segments 
        return parsed_text

    def skip_to_next_part(self):
        """
        Skip to the next part of the dialogue.
        """
        if not self.is_on_last_part() and self.char_count >= len(self.current_dialogue_part):  # If not on the last part and all characters are shown
            self.part_ind += 1
            self.current_dialogue_part = self.textes[self.part_ind]  # Current text to be shown
            self.parsed_dialogue_part = self.parse_text(self.current_dialogue_part)  # Parsed text to be shown
            self.char_count = 0
            self.segmented_text = [''] * (len(self.current_dialogue_part) // MAX_LINE_SIZE + 1)
            self.character_sprite = choice(self.sprites_choices)


    def reset(self):
        """
        Reset the dialogue to the beginning.
        """
        self.current_dialogue_part = self.textes[0]
        self.char_count = 0
        self.segmented_text = [''] * (len(self.current_dialogue_part) // MAX_LINE_SIZE + 1)
        self.part_ind = 0
    
    def draw(self, screen: pg.Surface):
        """
        Draw the dialogue and bot animation on the screen.
        """

        character_sprite_rect = self.character_sprite.get_rect(bottomleft=(0, 1080))
        screen.blit(self.character_sprite, character_sprite_rect)

        screen.blit(pg.Surface((0,0), pg.SRCALPHA), (300, 750))  #TODO: Replace with actual background image

        for i, surf in enumerate(self.bliting_list[-5:]):
            line_height = 812 + 27 * i  # Calculate the line height
            screen.blit(surf, (300, line_height))  # Draw each line of the dialogue
    
    def click_interaction(self) -> bool:
        """
        Handle click interaction and return True if the dialogue is finished.
        """
        if self.is_on_last_part():
            return True  # Dialogue is finished
        else:
            self.skip_to_next_part()  # Skip to the next part of the dialogue
            return False

#parsing tests
if __name__ == '__main__':
    d = Dialogue([''])
    print(d.parse_text('Hello /b/World/ This is a test /i/italic/ text.'), 1, 5)