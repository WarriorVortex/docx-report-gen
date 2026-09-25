"""Table mixin with optional captions."""
from ..styles import CAPTION_STYLE_NAME
from ._base import DocMixin
from .utils import render_caption


class TableMixin(DocMixin):
    """Adds table() to Report.

    Captioned tables are numbered automatically: the first captioned
    table becomes 1, the next 2, and so on. Uncaptered tables do not
    consume a number.
    """

    _table_counter = 0

    def table(self, data, caption: str | None = None,
              style: str = 'Table Grid', header: bool = True):
        """Insert a table, optionally preceded by a numbered caption."""
        if caption is not None:
            self._table_counter += 1
            para = render_caption(
                self.doc, self.config.caption, CAPTION_STYLE_NAME,
                self._table_counter, caption,
            )
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