from pygame import font
font.init()

import sys, os

print(sys.path)
print(os.path.abspath(__file__))
print(sys._MEIPASS if hasattr(sys, '_MEIPASS') else '')

font_path = "data/PxPlus_IBM_VGA8.ttf"
font_size = 35

DIALOGUE_FONT = font.Font("nimbus-sans-l.regular.otf", font_size)
DIALOGUE_FONT_BOLD = font.Font("nimbus-sans-l.bold.otf", font_size)
DIALOGUE_FONT_ITALIC = font.Font("nimbus-sans-l.regular-italic.otf", font_size)
BUTTON_FONT = font.SysFont('arial', font_size)
STANDARD_COLOR = (255, 212, 163)