"""Apply StylesConfig to a python-docx Document.

The public entry point is `apply()`. Each category of styles lives in
its own module (normal, title, headings, captions, page) and exposes a
single `apply_*` function. To add a new category, create the module
and add one import + one call below.
"""
from docx import Document

from ..config import StylesConfig
from .captions import apply_captions
from .headings import apply_headings
from .normal import apply_normal
from .page import apply_margins
from .title import apply_title


def apply(doc: Document, config: StylesConfig) -> None:
    """Apply a StylesConfig to every relevant style of the document."""
    apply_normal(doc, config)
    apply_title(doc, config)
    apply_headings(doc, config)
    apply_captions(doc, config)
    apply_margins(doc, config)


__all__ = ['apply']