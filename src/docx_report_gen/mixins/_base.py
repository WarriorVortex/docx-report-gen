"""Shared base for Report mixins."""
from docx import Document


class DocMixin:
    """Base for mixins operating on the `doc` attribute.

    Declares `doc: Document` at class level so that type checkers and
    IDEs see the correct type of `self.doc` inside every mixin.
    The actual value is assigned in Report.__init__.
    """

    doc: Document