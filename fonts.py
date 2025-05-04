from pygame import font
font.init()
import sys, os

folder = 'assets/'

font_path = "data/PxPlus_IBM_VGA8.ttf"
font_size = 35

DIALOGUE_FONT = font.Font(folder+"nimbus-sans-l.regular.otf", font_size)
DIALOGUE_FONT_BOLD = font.Font(folder+"nimbus-sans-l.bold.otf", font_size)
DIALOGUE_FONT_ITALIC = font.Font(folder+"nimbus-sans-l.regular-italic.otf", font_size)
DESCRIPTION_FONT = font.Font(folder+"nimbus-sans-l.regular.otf", font_size-10)
BUTTON_FONT = font.SysFont('arial', font_size)
BIG_FONT = font.Font(folder+"nimbus-sans-l.regular-italic.otf", font_size*2)
STANDARD_COLOR = (255, 212, 163)