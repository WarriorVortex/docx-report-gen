"""Layout methods mixin."""
from .._xml import add_page_number, set_paragraph_bottom_border
from ..styles import ALIGN
from ._base import DocMixin


class LayoutMixin(DocMixin):
    """Adds page_break(), hr(), header(), footer(), page_numbers()
    to Report."""

    def page_break(self):
        """Insert a page break."""
        self.doc.add_page_break()
        return self

    def hr(self):
        """Insert a horizontal rule (bottom-bordered empty paragraph)."""
        para = self.doc.add_paragraph()
        set_paragraph_bottom_border(para)
        return self

    def header(self, text, align='center'):
        """Set header text for all sections."""
        for section in self.doc.sections:
            section.header.is_linked_to_previous = False
            para = section.header.paragraphs[0]
            para.text = ''
            para.alignment = ALIGN[align]
            para.add_run(text)
        return self

    def footer(self, text=None, align='center'):
        """Set footer text (page number is added separately)."""
        for section in self.doc.sections:
            section.footer.is_linked_to_previous = False
            para = section.footer.paragraphs[0]
            para.text = ''
            para.alignment = ALIGN[align]
            if text:
                para.add_run(text)
        return self

    def page_numbers(self, align='center', skip_first=True):
        """Insert page numbers into the footer.

        `skip_first=True` suppresses header and footer on the first
        page — useful for title pages.
        """
        for section in self.doc.sections:
            if skip_first:
                section.different_first_page_header_footer = True
            section.footer.is_linked_to_previous = False
            para = section.footer.paragraphs[0]
            para.alignment = ALIGN[align]
            add_page_number(para)
        return self