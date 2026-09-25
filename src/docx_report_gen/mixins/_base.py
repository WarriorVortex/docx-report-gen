"""Shared base for Report mixins.

Declares `doc` and `config` at class level so that type checkers and
IDEs see the correct attribute types inside every mixin. Actual values
are assigned in Report.__init__.

This class deliberately has no methods: shared behavior belongs in
mixins/utils.py, not on the base.
"""
from docx import Document

from ..styles import StylesConfig


class DocMixin:
    doc: Document
    config: StylesConfig