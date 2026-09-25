"""Report class — assembles all mixins into a single builder."""
from docx import Document

from .mixins import HeadingMixin, ParagraphMixin, TableMixin
from .styles import configure_fonts, set_margins


class Report(HeadingMixin, ParagraphMixin, TableMixin):
    """Declarative docx report builder.

    Example:
        from docx_report_gen import Report, b, i, f

        r = Report()
        r.h1('Introduction')
        r.p('The ', b('key'), ' relation is ', f('E = mc^2'), '.')
        r.f(r'\\int_0^1 x^2 \\, dx')   # block formula
        r.save('report.docx')
    """

    def __init__(
        self,
        font: str = 'Times New Roman',
        size: int = 12,
        h_sizes: tuple = (18, 16, 14, 13, 12, 12),
        margins: tuple | None = None,
    ):
        self.doc = Document()
        configure_fonts(self.doc, font, size, h_sizes)
        if margins:
            set_margins(self.doc, *margins)

    def style(self, name: str):
        """Direct access to a python-docx style object."""
        return self.doc.styles[name]

    def page_break(self):
        self.doc.add_page_break()
        return self

    def save(self, path: str):
        self.doc.save(path)