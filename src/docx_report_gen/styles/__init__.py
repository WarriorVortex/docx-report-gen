"""Style configuration, resolution and application."""
from .apply import apply
from .config import (
    CaptionStyle, HeadingStyle, ImageStyle, ParagraphStyle, StylesConfig,
)
from .constants import (
    ALIGN, CAPTION_STYLE_NAME, IMAGE_CAPTION_STYLE_NAME,
)
from .resolvers import (
    resolve_caption, resolve_formula, resolve_heading,
    resolve_image, resolve_image_caption, resolve_paragraph,
    resolve_title,
)
from .utils import resolve

__all__ = [
    'ALIGN',
    'CAPTION_STYLE_NAME',
    'IMAGE_CAPTION_STYLE_NAME',
    'apply',
    'resolve',
    'resolve_title',
    'resolve_heading',
    'resolve_paragraph',
    'resolve_formula',
    'resolve_caption',
    'resolve_image_caption',
    'resolve_image',
    'CaptionStyle',
    'HeadingStyle',
    'ImageStyle',
    'ParagraphStyle',
    'StylesConfig',
]