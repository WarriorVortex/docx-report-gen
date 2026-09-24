"""Report class — a minimal API for generating docx reports."""
import re
from docx import Document
import math2docx

from .styles import ALIGN, configure_fonts, set_margins


# The math alternative comes first so that '*' characters inside $...$
# are not interpreted as markdown.
_INLINE_PATTERN = re.compile(
    r'(?P<math>\$[^$]+\$)'
    r'|(?P<bold>\*\*[^*]+\*\*)'
    r'|(?P<italic>\*[^*]+\*)'
)


class Report:
    """Declarative docx report builder.

    Example:
        r = Report()
        r.title('Report').h1('Introduction').p('Text with $E=mc^2$')
        r.save('report.docx')
    """

    def __init__(
        self,
        font: str = 'Times New Roman',
        size: int = 12,
        h_sizes: tuple = (20, 16, 14),
        margins: tuple | None = None,
    ):
        self.doc = Document()
        configure_fonts(self.doc, font, size, h_sizes)
        if margins:
            set_margins(self.doc, *margins)

    # ---------- fine tuning ----------
    def style(self, name: str):
        """Direct access to a python-docx style object."""
        return self.doc.styles[name]

    # ---------- headings ----------
    def title(self, text: str, align: str = 'center'):
        self.doc.add_heading(text, level=0).alignment = ALIGN[align]
        return self

    def h1(self, text: str, align: str | None = None):
        self.doc.add_heading(text, level=1).alignment = ALIGN[align]
        return self

    def h2(self, text: str, align: str | None = None):
        self.doc.add_heading(text, level=2).alignment = ALIGN[align]
        return self

    def h3(self, text: str, align: str | None = None):
        self.doc.add_heading(text, level=3).alignment = ALIGN[align]
        return self

    # ---------- content ----------
    def p(self, text: str = '', align: str = 'justify'):
        para = self.doc.add_paragraph()
        para.alignment = ALIGN[align]
        self._inline(para, text)
        return self

    def f(self, latex: str, align: str = 'center'):
        """Block formula on its own line."""
        para = self.doc.add_paragraph()
        para.alignment = ALIGN[align]
        math2docx.add_math(para, latex)
        return self

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

    def page_break(self):
        self.doc.add_page_break()
        return self

    def save(self, path: str):
        self.doc.save(path)

    # ---------- internals ----------
    def _inline(self, para, text: str):
        """Parse $formula$, **bold**, *italic* inside a string."""
        pos = 0
        for m in _INLINE_PATTERN.finditer(text):
            if m.start() > pos:
                para.add_run(text[pos:m.start()])
            if m.group('math'):
                math2docx.add_math(para, m.group('math')[1:-1])
            elif m.group('bold'):
                para.add_run(m.group('bold')[2:-2]).bold = True
            elif m.group('italic'):
                para.add_run(m.group('italic')[1:-1]).italic = True
            pos = m.end()
        if pos < len(text):
            para.add_run(text[pos:])