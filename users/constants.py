import os

from team_finder import settings

NAME_MAX_LENGTH = 124

FONTS_DIR = os.path.join(settings.BASE_DIR, 'static', 'fonts',
                         'Neue_Haas_Grotesk_Display_Pro_75_Bold.otf')

IMAGE_WIDTH = 100
IMAGE_HEIGHT = 100

COLORS = [
    ('black', 'white'),
    ('green', 'blue'),
    ('yellow', 'black')
]

TEXT_BACKGROUND_RATIO = 0.6
