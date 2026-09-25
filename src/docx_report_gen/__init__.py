"""docx-report-gen — a minimal wrapper for generating docx reports."""
from .inline import b, i, f
from .report import Report

__all__ = ['Report', 'b', 'i', 'f']
__version__ = '0.2.0'