"""Style configuration dataclasses."""
from .caption import CaptionStyle
from .code import CodeStyle
from .document import StylesConfig
from .heading import HeadingStyle
from .image import ImageStyle
from .list import ListStyle
from .paragraph import ParagraphStyle
from .quote import QuoteStyle
from .types import RGB

__all__ = [
    'RGB',
    'HeadingStyle',
    'CaptionStyle',
    'ParagraphStyle',
    'ImageStyle',
    'ListStyle',
    'CodeStyle',
    'QuoteStyle',
    'StylesConfig',
]