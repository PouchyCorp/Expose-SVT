from pygame import Surface
from ui.sprite import WINDOW, nine_slice_scaling
from utils.fonts import TERMINAL_FONT

class InfoPopup:
    def __init__(self, text):
        """Initializes the popup with the given text.  
        Put it in the game's popups list to display it."""

        self.text : str = text
        
        self.text_surf = TERMINAL_FONT.render(self.text, False, "white")
        txt_rect = self.text_surf.get_rect()
        self.bg_surf = nine_slice_scaling(WINDOW,(txt_rect.w+30, txt_rect.h+30), (12, 12, 12, 12))
        self.bg_surf.blit(self.text_surf, (18,18))

        self.rect = self.bg_surf.get_rect(center=(1920//2, -100))

        self.lifetime : int = 300

    def draw(self, screen : Surface):
        """Draws the popup on the screen.  
        Clever use of the lifetime attribute to program the popup's behavior."""
        self.lifetime -= 1
        
        if self.lifetime >= 75:
            self.rect.y = min(50, self.rect.y+10)
        else:
            self.rect.y -= 10
            
        screen.blit(self.bg_surf, self.rect)
