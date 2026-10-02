"""Report class — assembles all mixins into a single builder."""
from typing import Any, Optional

from docx import Document

from .docx import DocxDocument
from .metadata import DocumentMetadata, apply_metadata
from .mixins import (
    BookmarkMixin, CodeMixin, HeadingMixin, ImageMixin, LayoutMixin,
    ListMixin, ParagraphMixin, PluginMixin, TableMixin, TocMixin,
)
from .plugins import Plugin
from .styles import StylesConfig, apply


class Report(HeadingMixin, ParagraphMixin, ListMixin, CodeMixin,
              TableMixin, ImageMixin, BookmarkMixin, TocMixin,
              LayoutMixin, PluginMixin):
    """Declarative docx report builder."""

    doc: DocxDocument

    def __init__(
        self,
        config: Optional[StylesConfig] = None,
        metadata: Optional[DocumentMetadata] = None,
        plugins: Optional[list[Plugin]] = None,
    ) -> None:
        self.config = config or StylesConfig()
        self.metadata = metadata or DocumentMetadata()
        self.doc = Document()

        # Cooperative init: stateful mixins set their private state
        # here. The MRO chain runs each __init__ exactly once.
        super().__init__()

        apply(self.doc, self.config)
        apply_metadata(self.doc, self.metadata)

        # Plugins must see a fully configured document.
        self._init_plugins(plugins)

    def style(self, name: str) -> Any:
        """Direct access to a python-docx style object."""
        return self.doc.styles[name]

    def save(self, path: str) -> None:
        """Write the document, running plugin save hooks around it."""
        self._plugins_before_save(path)
        self.doc.save(path)
        self._plugins_after_save(path)