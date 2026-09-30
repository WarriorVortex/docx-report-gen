"""Table of contents mixin."""
from .._xml import (
    add_toc, mark_fields_dirty, set_update_fields_on_open,
)
from ._base import DocMixin


class TocMixin(DocMixin):
    """Adds toc() and update_toc() to Report.

    The TOC is a Word field: it is rendered by the reader (Word or
    LibreOffice), not by the generator. Two mechanisms control when
    it is refreshed:

      - per-field dirty flag — Word refreshes the field on open;
      - document setting `updateFields` — Word refreshes *all* fields
        on open.

    `toc()` sets the dirty flag by default. `update_toc()` re-marks
    every field in the document and enables the document-level flag;
    call it before save() if you want the strongest guarantee.
    """

    def toc(self, title=None, levels='1-3'):
        """Insert a table-of-contents field.

        Args:
            title: optional heading above the TOC. Uses Word's
                "TOC Heading" style when available; falls back to a
                bold paragraph otherwise, so the title itself does
                not appear inside the TOC.
            levels: heading levels to include, e.g. '1-3'.

        Word updates the field on open, or manually via F9.
        LibreOffice: Edit → Update Fields.
        """
        if title:
            self._add_toc_heading(title)
        para = self.doc.add_paragraph()
        add_toc(para, levels, dirty=True)
        return self

    def update_toc(self):
        """Force Word to refresh every field when the document is opened.

        Sets the dirty flag on all fields in the document and enables
        the document-wide `updateFields` setting. Use this before
        save() if you have modified the document after inserting the
        TOC (for example, added headings further down).

        Both mechanisms are idempotent: calling update_toc() twice
        produces the same result.
        """
        for para in self.doc.paragraphs:
            mark_fields_dirty(para)
        set_update_fields_on_open(self.doc, True)
        return self

    def _add_toc_heading(self, text):
        """Add a heading that does not appear inside the TOC itself."""
        try:
            self.doc.add_paragraph(text, style='TOC Heading')
        except KeyError:
            para = self.doc.add_paragraph()
            run = para.add_run(text)
            run.bold = True