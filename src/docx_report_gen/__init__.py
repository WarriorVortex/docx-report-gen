"""docx-report-gen — a minimal wrapper for generating docx reports."""
from .inline import b, i, f
from .report import Report
from .styles import HeadingStyle, StylesConfig

__all__ = ['Report', 'StylesConfig', 'HeadingStyle', 'b', 'i', 'f']
__version__ = '0.2.0'