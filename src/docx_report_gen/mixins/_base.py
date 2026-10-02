"""Shared base for Report mixins.

DocMixin declares the minimum contract that every mixin relies on:
`doc` and `config`. All values are assigned in Report.__init__.
"""
from ..docx import DocxDocument
from ..styles import StylesConfig


class DocMixin:
    """Base for mixins operating on `doc` and `config`."""
    doc: DocxDocument
    config: StylesConfig