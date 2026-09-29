"""Style configuration dataclasses."""
from .caption import CaptionStyle
from .document import StylesConfig
from .heading import HeadingStyle
from .image import ImageStyle
from .paragraph import ParagraphStyle
from .types import RGB

__all__ = [
    'RGB',
    'HeadingStyle',
    'CaptionStyle',
    'ParagraphStyle',
    'ImageStyle',
    'StylesConfig',
]