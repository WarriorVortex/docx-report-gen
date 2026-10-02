"""Layout methods mixin."""
from typing import Optional

from .._utils import (
    add_page_break, add_page_number, set_paragraph_bottom_border,
)
from ..styles import ALIGN, AlignLiteral
from ._base import DocMixin


class LayoutMixin(DocMixin):
    """Adds page_break(), hr(), header(), footer(), page_numbers()."""

    def page_break(self) -> 'LayoutMixin':
        """Insert a page break."""
        add_page_break(self.doc)
        return self

    def hr(self) -> 'LayoutMixin':
        """Insert a horizontal rule."""
        para = self.doc.add_paragraph()
        set_paragraph_bottom_border(para)
        return self

    def header(self, text: str,
               align: AlignLiteral = 'center') -> 'LayoutMixin':
        """Set header text for all sections."""
        for section in self.doc.sections:
            section.header.is_linked_to_previous = False
            para = section.header.paragraphs[0]
            para.text = ''
            alignment = ALIGN[align]
            if alignment is not None:
                para.alignment = alignment
            para.add_run(text)
        return self

    def footer(self, text: Optional[str] = None,
               align: AlignLiteral = 'center') -> 'LayoutMixin':
        """Set footer text."""
        for section in self.doc.sections:
            section.footer.is_linked_to_previous = False
            para = section.footer.paragraphs[0]
            para.text = ''
            alignment = ALIGN[align]
            if alignment is not None:
                para.alignment = alignment
            if text:
                para.add_run(text)
        return self

    def page_numbers(self, align: AlignLiteral = 'center',
                     skip_first: bool = True) -> 'LayoutMixin':
        """Insert page numbers into the footer."""
        for section in self.doc.sections:
            if skip_first:
                section.different_first_page_header_footer = True
            section.footer.is_linked_to_previous = False
            para = section.footer.paragraphs[0]
            alignment = ALIGN[align]
            if alignment is not None:
                para.alignment = alignment
            add_page_number(para)
        return self