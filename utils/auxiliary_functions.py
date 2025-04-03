import random
import re

from django.core.exceptions import ValidationError


def generate_random_color():
    return "#" + ''.join([random.choice('0123456789ABCDEF') for _ in range(6)])


def is_bright_color(hex_color: str) -> bool:
    hex_color = hex_color.lstrip('#')
    if len(hex_color) != 6:
        raise ValueError(f"Ungültiger Hex-Wert: {hex_color}")  
    
    r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))  
    brightness = (r * 299 + g * 587 + b * 114) / 1000  

    return brightness > 128


def validate_hex_color(value):
    if not re.match(r'^#[0-9A-Fa-f]{6}$', value):
        raise ValidationError("Color must be a valid hex code in the format #RRGGBB.")