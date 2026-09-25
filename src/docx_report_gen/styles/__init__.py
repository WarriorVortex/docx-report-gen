"""Style configuration and application."""
from .apply import apply
from .config import CaptionStyle, HeadingStyle, StylesConfig
from .constants import (
    ALIGN, CAPTION_STYLE_NAME, IMAGE_CAPTION_STYLE_NAME,
)

__all__ = [
    'ALIGN',
    'CAPTION_STYLE_NAME',
    'IMAGE_CAPTION_STYLE_NAME',
    'apply',
    'CaptionStyle',
    'HeadingStyle',
    'StylesConfig',
]