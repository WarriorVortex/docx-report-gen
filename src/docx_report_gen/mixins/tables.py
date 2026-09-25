"""Table mixin."""
from ._base import DocMixin


class TableMixin(DocMixin):
    """Adds table() to Report."""

    def table(self, data, style: str = 'Table Grid', header: bool = True):
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