"""Table of contents mixin."""
from typing import Optional

from .._utils import (
    add_toc, mark_fields_dirty, set_update_fields_on_open,
)
from ._base import DocMixin


class TocMixin(DocMixin):
    """Adds toc() and update_toc() to Report."""

    def toc(self, title: Optional[str] = None,
            levels: str = '1-3') -> 'TocMixin':
        """Insert a table-of-contents field."""
        if title:
            self._add_toc_heading(title)
        para = self.doc.add_paragraph()
        add_toc(para, levels, dirty=True)
        return self

    def update_toc(self) -> 'TocMixin':
        """Force Word to refresh every field when the document opens."""
        for para in self.doc.paragraphs:
            mark_fields_dirty(para)
        set_update_fields_on_open(self.doc, True)
        return self

    def _add_toc_heading(self, text: str) -> None:
        try:
            self.doc.add_paragraph(text, style='TOC Heading')
        except KeyError:
            para = self.doc.add_paragraph()
            run = para.add_run(text)
            run.bold = True