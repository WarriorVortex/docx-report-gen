"""docx-report-gen — a minimal wrapper for generating docx reports."""
from importlib.metadata import version, PackageNotFoundError

from .inline import b, i, f, link
from .metadata import DocumentMetadata
from .report import Report
from .styles import (
    CaptionStyle, CodeStyle, HeadingStyle, ImageStyle,
    ListStyle, ParagraphStyle, QuoteStyle, StylesConfig,
)

try:
    __version__ = version("docx-report-gen")
except PackageNotFoundError:
    __version__ = "0.0.0+unknown"

__all__ = [
    'Report',
    'StylesConfig',
    'DocumentMetadata',
    'HeadingStyle',
    'CaptionStyle',
    'ParagraphStyle',
    'ImageStyle',
    'ListStyle',
    'CodeStyle',
    'QuoteStyle',
    'b', 'i', 'f', 'link',
]