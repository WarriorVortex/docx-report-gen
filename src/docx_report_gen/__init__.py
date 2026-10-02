"""docx-report-gen — a minimal wrapper for generating docx reports."""
from importlib.metadata import version, PackageNotFoundError

from . import docx
from . import writer
from .inline import (
    b, i, u, s, sup, sub, color, highlight, f, link, ref,
)
from .metadata import DocumentMetadata
from .plugins import Plugin, PluginsRegistry
from .report import Report
from .styles import (
    CaptionStyle, CodeStyle, HeadingStyle, ImageStyle,
    LayoutStyle, ListStyle, ParagraphStyle, QuoteStyle,
    TableStyle, StylesConfig,
)

try:
    __version__ = version("docx-report-gen")
except PackageNotFoundError:
    __version__ = "0.0.0+unknown"

__all__ = [
    'Report',
    'Plugin',
    'PluginsRegistry',
    'StylesConfig',
    'DocumentMetadata',
    'HeadingStyle',
    'CaptionStyle',
    'ParagraphStyle',
    'ImageStyle',
    'ListStyle',
    'CodeStyle',
    'QuoteStyle',
    'TableStyle',
    'LayoutStyle',
    'b', 'i', 'u', 's', 'sup', 'sub', 'color', 'highlight',
    'f', 'link', 'ref',
    'docx',
    'writer',
]