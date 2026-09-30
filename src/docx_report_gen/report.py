"""Report class — assembles all mixins into a single builder."""
from docx import Document

from .metadata import DocumentMetadata, apply_metadata
from .mixins import (
    CodeMixin, HeadingMixin, ImageMixin, LayoutMixin,
    ListMixin, ParagraphMixin, TableMixin, TocMixin,
)
from .styles import StylesConfig, apply


class Report(HeadingMixin, ParagraphMixin, ListMixin, CodeMixin,
              TableMixin, ImageMixin, TocMixin, LayoutMixin):
    """Declarative docx report builder.

    Example:
        from docx_report_gen import Report, DocumentMetadata

        r = Report(
            metadata=DocumentMetadata(
                author='Иван Иванов',
                title='Лабораторная работа №1',
            ),
        )
        r.h1('Introduction')
        r.save('report.docx')
    """

    def __init__(self,
                 config: StylesConfig | None = None,
                 metadata: DocumentMetadata | None = None):
        self.config = config or StylesConfig()
        self.metadata = metadata or DocumentMetadata()
        self.doc = Document()
        apply(self.doc, self.config)
        apply_metadata(self.doc, self.metadata)

    def style(self, name: str):
        """Direct access to a python-docx style object."""
        return self.doc.styles[name]

    def save(self, path: str):
        self.doc.save(path)