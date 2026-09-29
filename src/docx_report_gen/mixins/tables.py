"""Table mixin with optional captions."""
from ..styles import CAPTION_STYLE_NAME, resolve_caption
from ._base import DocMixin
from .utils import render_caption


class TableMixin(DocMixin):
    """Adds table() to Report.

    Captioned tables are numbered automatically with a per-instance
    counter: the first captioned table becomes 1, the next 2, and so
    on. Uncaptered tables do not consume a number.
    """

    _table_counter = 0

    def table(self, data, caption=None, caption_align=None,
              style='Table Grid', header=True):
        """Insert a table, optionally preceded by a numbered caption.

        Args:
            data: list of rows; each row is a list of cell values.
            caption: caption text; None disables the caption.
            caption_align: local alignment override for the caption.
            style: python-docx table style name.
            header: if True, the first row is bolded.
        """
        if caption is not None:
            self._table_counter += 1
            cs = resolve_caption(self.config, {'align': caption_align})
            para = render_caption(
                self.doc, cs, CAPTION_STYLE_NAME,
                self._table_counter, caption,
            )
            # Keep caption on the same page as the following table.
            para.paragraph_format.keep_with_next = True

        rows, cols = len(data), len(data[0])
        t = self.doc.add_table(rows=rows, cols=cols)
        t.style = style
        for i, row in enumerate(data):
            for j, val in enumerate(row):
                cell = t.cell(i, j)
                cell.text = str(val)
                if i == 0 and header:
                    for para in cell.paragraphs:
                        for run in para.runs:
                            run.font.bold = True
        return self