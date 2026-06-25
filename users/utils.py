import io
from datetime import datetime
from random import choice

from PIL import Image, ImageDraw, ImageFont
from django.core.files.base import ContentFile

from . import constants


def generate_avatar(name):
    random_colors = choice(constants.COLORS)
    first_letter = name[0].upper()

    img = Image.new('RGB', (constants.IMAGE_WIDTH, constants.IMAGE_HEIGHT),
                    random_colors[0])
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(constants.FONTS_DIR,
                              size=constants.IMAGE_HEIGHT * constants.TEXT_BACKGROUND_RATIO)
    draw.text((constants.IMAGE_WIDTH // 2, constants.IMAGE_HEIGHT // 2),
              first_letter, fill=random_colors[1],
              font=font, anchor='mm')

    buffer = io.BytesIO()
    img.save(buffer, format='PNG')
    file_name = f"{first_letter}_{datetime.now()}_avatar.png"
    return ContentFile(buffer.getvalue(), name=file_name)
