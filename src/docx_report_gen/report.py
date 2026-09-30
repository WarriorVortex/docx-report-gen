"""Report class — assembles all mixins into a single builder."""
from docx import Document

from .mixins import (
    CodeMixin, HeadingMixin, ImageMixin, LayoutMixin,
    ListMixin, ParagraphMixin, TableMixin, TocMixin,
)
from .styles import StylesConfig, apply


class Report(HeadingMixin, ParagraphMixin, ListMixin, CodeMixin,
              TableMixin, ImageMixin, TocMixin, LayoutMixin):
    """Declarative docx report builder.

    Example:
        from docx_report_gen import Report, b, f, link

        r = Report()
        r.toc(title='Содержание', levels='1-2')
        r.h1('Introduction')
        r.p('See ', link('the spec', 'https://example.org'), '.')
        r.f(r'\\int_0^1 x^2 \\, dx', number=True)
        r.update_toc()
        r.save('report.docx')
    """

    def __init__(self, config: StylesConfig | None = None):
        self.config = config or StylesConfig()
        self.doc = Document()
        apply(self.doc, self.config)

    def style(self, name: str):
        """Direct access to a python-docx style object."""
        return self.doc.styles[name]

    def save(self, path: str):
        self.doc.save(path)