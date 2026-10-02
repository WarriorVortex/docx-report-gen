"""Style configuration, resolution and application."""
from .apply import apply
from .config import (
    CaptionStyle, CodeStyle, HeadingStyle, ImageStyle,
    LayoutStyle, ListStyle, ParagraphStyle, QuoteStyle,
    TableStyle, StylesConfig,
)
from .config.types import AlignLiteral, HexColor, Margins, PathLike, RGB
from .constants import (
    ALIGN, BOOKMARK_PREFIX, CAPTION_STYLE_NAME, CODE_STYLE_NAME,
    IMAGE_CAPTION_STYLE_NAME, LIST_BULLET_STYLES, LIST_NUMBER_STYLES,
    QUOTE_STYLE_NAME, SEQ_FIGURE, SEQ_TABLE,
)
from .resolvers import (
    resolve_caption, resolve_code, resolve_formula, resolve_heading,
    resolve_image, resolve_image_caption, resolve_list,
    resolve_paragraph, resolve_quote, resolve_table, resolve_title,
)
from .utils import resolve

__all__ = [
    'ALIGN',
    'BOOKMARK_PREFIX',
    'CAPTION_STYLE_NAME',
    'CODE_STYLE_NAME',
    'IMAGE_CAPTION_STYLE_NAME',
    'LIST_BULLET_STYLES',
    'LIST_NUMBER_STYLES',
    'QUOTE_STYLE_NAME',
    'SEQ_FIGURE',
    'SEQ_TABLE',
    'apply',
    'resolve',
    'resolve_title',
    'resolve_heading',
    'resolve_paragraph',
    'resolve_formula',
    'resolve_caption',
    'resolve_image_caption',
    'resolve_image',
    'resolve_list',
    'resolve_code',
    'resolve_quote',
    'resolve_table',
    'AlignLiteral',
    'HexColor',
    'Margins',
    'PathLike',
    'RGB',
    'CaptionStyle',
    'CodeStyle',
    'HeadingStyle',
    'ImageStyle',
    'LayoutStyle',
    'ListStyle',
    'ParagraphStyle',
    'QuoteStyle',
    'TableStyle',
    'StylesConfig',
]