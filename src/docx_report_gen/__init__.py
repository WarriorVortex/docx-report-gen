"""docx-report-gen — a minimal wrapper for generating docx reports."""
from .inline import b, i, f, link
from .report import Report
from .styles import (
    CaptionStyle, CodeStyle, HeadingStyle, ImageStyle,
    ListStyle, ParagraphStyle, QuoteStyle, StylesConfig,
)

__all__ = [
    'Report',
    'StylesConfig',
    'HeadingStyle',
    'CaptionStyle',
    'ParagraphStyle',
    'ImageStyle',
    'ListStyle',
    'CodeStyle',
    'QuoteStyle',
    'b', 'i', 'f', 'link',
]
__version__ = '0.2.1'