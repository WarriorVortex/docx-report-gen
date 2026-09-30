"""docx-report-gen — a minimal wrapper for generating docx reports."""
from .inline import b, i, f, link
from .report import Report
from .styles import (
    CaptionStyle, CodeStyle, HeadingStyle, ImageStyle,
    ListStyle, ParagraphStyle, QuoteStyle, StylesConfig,
)
from importlib.metadata import version, PackageNotFoundError

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

try:
    __version__ = version("docx-report-gen")
except PackageNotFoundError:
    __version__ = "0.0.0+unknown"