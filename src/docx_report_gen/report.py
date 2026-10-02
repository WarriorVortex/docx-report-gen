"""Report class — assembles all mixins into a single builder."""
from docx import Document

from .metadata import DocumentMetadata, apply_metadata
from .mixins import (
    BookmarkMixin, CodeMixin, HeadingMixin, ImageMixin, LayoutMixin,
    ListMixin, ParagraphMixin, TableMixin, TocMixin,
)
from .styles import StylesConfig, apply


class Report(HeadingMixin, ParagraphMixin, ListMixin, CodeMixin,
              TableMixin, ImageMixin, BookmarkMixin, TocMixin,
              LayoutMixin):
    """Declarative docx report builder.

    Example:
        from docx_report_gen import Report, ref

        r = Report()
        r.p('See table ', ref('results'), ' below.')
        r.table([[1, 2]], caption='Measurements', name='results')
        r.save('report.docx')
    """

    def __init__(self,
                 config: StylesConfig | None = None,
                 metadata: DocumentMetadata | None = None):
        self.config = config or StylesConfig()
        self.metadata = metadata or DocumentMetadata()
        self.doc = Document()
        self._init_bookmarks()
        apply(self.doc, self.config)
        apply_metadata(self.doc, self.metadata)

    def style(self, name: str):
        """Direct access to a python-docx style object."""
        return self.doc.styles[name]

    def save(self, path: str):
        self.doc.save(path)