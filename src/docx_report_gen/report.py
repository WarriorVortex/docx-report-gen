"""Report class — assembles all mixins into a single builder."""
from docx import Document

from .mixins import (
    HeadingMixin, ImageMixin, LayoutMixin,
    ParagraphMixin, TableMixin,
)
from .styles import StylesConfig, apply


class Report(HeadingMixin, ParagraphMixin, TableMixin, ImageMixin,
              LayoutMixin):
    """Declarative docx report builder.

    Example:
        from docx_report_gen import Report, StylesConfig, b, f

        config = StylesConfig(font='Times New Roman')
        r = Report(config=config)
        r.h1('Introduction')
        r.p('The ', b('key'), ' relation is ', f('E = mc^2'), '.')
        r.img('plot.png', caption='Dependency plot', width=12)
        r.table([[1, 2], [3, 4]], caption='Experimental data')
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