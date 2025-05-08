import pygame as pg
from fonts import DIALOGUE_FONT, DIALOGUE_FONT_BOLD, DIALOGUE_FONT_ITALIC, DESCRIPTION_FONT, BIG_FONT
from file_loader import load_and_resize_image, load_image
from random import choice

MAX_LINE_SIZE = 100  # Maximum number of characters per line
PAGE_SIZE = 5  # Number of lines per page

DIALOG_BG = load_image('dialogwindow.png')

pg.mixer.music.load('assets/voice.mp3')
pg.mixer.music.set_volume(0.2)  # Set the volume of the voice
pg.mixer.music.play(-1)  # Play the voice in a loop
pg.mixer.music.pause()  # Pause the voice


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

            case 'Jean-Jaques Jet-Stream':
                self.sprites_choices = [load_and_resize_image("riche1.png"), load_and_resize_image("riche2.png"), load_and_resize_image("riche3.png"), load_and_resize_image("riche4.png")]
            
            case 'Professeur Paleo-Climat':
                self.sprites_choices = [load_and_resize_image("sdf1.png"), load_and_resize_image("sdf2.png"), load_and_resize_image("sdf3.png"), load_and_resize_image("sdf4.png")]
            
            case 'Villageois':
                self.sprites_choices = [load_and_resize_image("pnj1.png"), load_and_resize_image("pnj2.png")]

            case 'Maire':
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
            if len(segment[0]) >= stop:
                cropped_text.append([segment[0][:stop+1], segment[1]])
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
                case 4:  # Red bold text
                    surf_list.append(DIALOGUE_FONT_BOLD.render(segment, False, 'red'))
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
        if self.char_count <= len(self.current_dialogue_part):  # If there are remaining characters to be shown
            pg.mixer.music.unpause()  # Unpause the voice
            visible_text = self.crop_parsed_text(self.parsed_dialogue_part, 0, self.char_count)
            lines = []
            current_line = []
            current_line_length = 0

            for segment, segment_type in visible_text:
                words = segment.split(' ')
                for i, word in enumerate(words):
                    word_length = len(word) + (1 if current_line or i > 0 else 0)  # Account for space if not the first word
                    if current_line_length + word_length <= MAX_LINE_SIZE:
                        if i > 0 or current_line:  # Add a space before the word if it's not the first word in the segment
                            current_line.append((' ', 0))
                            current_line_length += 1
                        current_line.append((word, segment_type))
                        current_line_length += len(word)
                    else:
                        lines.append(current_line)
                        current_line = [(word, segment_type)]
                        current_line_length = len(word)

            if current_line:
                lines.append(current_line)

            self.segmented_text = lines
            self.char_count += 1  # Increment the character count
        else:
            pg.mixer.music.pause()
        
        self.bliting_list = []  # Reset bliting list
        for line in self.segmented_text:
            self.bliting_list.append(self.get_text_surf(line))

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
        parsed_text : list[list]= [['', 0]]  # List of tuples (text, status) 0: normal, 1: bold, 2: italic, 3: red
        i = 0  # Index for the text
        while i < len(text):
            for sig, sig_ind in [('b', 1), ('i', 2), ('r', 3), ('a', 4)]:
                if i < len(text)-1 and text[i] == '/' and text[i+1] == sig:
                    i += 3  # Skip the esc characters ('/', sig, '/')
                    parsed_text.append(['', sig_ind])
                    while i < len(text) and text[i] != '/':
                        parsed_text[-1][0] += text[i]
                        i += 1
                    if i < len(text) and text[i] == '/':  # Ensure we don't go out of bounds
                        i += 1  # Skip the '/' character
                    parsed_text.append(['', 0])
                    break
            
            if i >= len(text):  # Ensure we don't access out of bounds
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

        character_sprite_rect = self.character_sprite.get_rect(bottomleft=(30, 960))
        screen.blit(self.character_sprite, character_sprite_rect)

        screen.blit(DIALOG_BG, (0,0))

        for i, doc in enumerate(self.documents):
            doc_surf, doc_name = doc
            padding = 10  # Padding between documents
            row = i // 4  # Determine the row (0-based index)
            col = i % 4   # Determine the column (0-based index)
            x_offset = 1820 - (col * (doc_surf.get_width() + padding))  # Adjust x position for each column
            y_offset = 100 + (row * (doc_surf.get_height() + padding))  # Adjust y position for each row

            doc_rect = doc_surf.get_rect(topright=(x_offset, y_offset))
            screen.blit(doc_surf, doc_rect)

            # Render and position the document name below the document
            doc_name_surf = DESCRIPTION_FONT.render(doc_name, True, 'gray')
            doc_name_rect = doc_name_surf.get_rect(midtop=(doc_rect.centerx, doc_rect.bottom + 5))
            screen.blit(doc_name_surf, doc_name_rect)
        
        character_name_sprite = BIG_FONT.render(self.character_name, True, (200, 147, 42))
        character_name_rect = character_name_sprite.get_rect(center=(400, 670))  # Center the character name at the bottom of the screen
        screen.blit(character_name_sprite, character_name_rect)

        for i, surf in enumerate(self.bliting_list[-5:]):
            line_height = 775 + 45 * i  # Calculate the line height
            screen.blit(surf, (91, line_height))  # Draw each line of the dialogue
    
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