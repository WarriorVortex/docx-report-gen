"""Report class — assembles all mixins into a single builder."""
from pathlib import Path
from typing import Optional, Union

from docx import Document

from .docx import DocxDocument
from .metadata import DocumentMetadata
from .metadata import apply_metadata as apply_metadata_to_doc
from .mixins import (
    BookmarkMixin, CodeMixin, HeadingMixin, ImageMixin, LayoutMixin,
    ListMixin, ParagraphMixin, PluginMixin, TableMixin, TocMixin,
)
from .plugins import Plugin
from .styles import StylesConfig, apply


SourceType = Union[str, Path, DocxDocument]
"""Anything accepted as the Report's source document.

    - a filesystem path (str or Path) to a .docx file
    - an already-opened DocxDocument instance
    - None (empty document)
"""


def _load_source(source: SourceType) -> DocxDocument:
    """Return a DocxDocument from a path, or pass through an existing one."""
    if isinstance(source, DocxDocument):
        return source
    return Document(str(source))


class Report(HeadingMixin, ParagraphMixin, ListMixin, CodeMixin,
              TableMixin, ImageMixin, BookmarkMixin, TocMixin,
              LayoutMixin, PluginMixin):
    """Declarative docx report builder.

    The Report may start from an empty document (default) or from an
    existing .docx file. When `source` is given, the file's entire
    content becomes the base — all its styles, docDefaults, headers,
    images and sections are preserved as-is. New content added through
    the API is appended after it.

        # Empty document
        r = Report()

        # From an existing .docx (title page, template, anything)
        r = Report(source='Титульный лист.docx')
        r.h1('Введение')
        r.save('report.docx')

        # Replace the document later
        r.set_source('другой.docx')
        r.set_document(Document('третий.docx'))

    Config and metadata can be set at construction time or changed
    later:

        r = Report(config=cfg, metadata=md)
        r.set_config(other_cfg)      # re-applies styles
        r.set_metadata(other_md)     # applied at save()

    Plugins:
        from docx_report_gen.plugins import plugins, Plugin

        class TocPlugin(Plugin):
            name = 'auto-toc'
            def setup(self, report):
                report.toc(title='Содержание', levels='1-2')

        plugins.register(TocPlugin())

        r = Report()
        r.h1('Introduction')
        r.save('report.docx')
        r.close()
    """

    doc: DocxDocument
    config: StylesConfig
    metadata: DocumentMetadata

    def __init__(
        self,
        config: Optional[StylesConfig] = None,
        metadata: Optional[DocumentMetadata] = None,
        plugins: Optional[list[Plugin]] = None,
        source: Optional[SourceType] = None,
    ) -> None:
        """Create a Report.

        Args:
            config: StylesConfig for the document. Defaults to a new
                StylesConfig with library defaults.
            metadata: DocumentMetadata for core properties.
            plugins: additional plugins for this Report only.
            source: optional base document. A path to a .docx, or an
                already-opened Document. When given, the Report's
                document is that file (loaded as-is); when None, an
                empty Document is created.
        """
        self.config = config or StylesConfig()
        self.metadata = metadata or DocumentMetadata()

        if source is None:
            self.doc = Document()
        else:
            self.doc = _load_source(source)

        # Cooperative init: stateful mixins set their private state
        # here. The MRO chain runs each __init__ exactly once.
        super().__init__()

        apply(self.doc, self.config)
        apply_metadata_to_doc(self.doc, self.metadata)

        # Plugins must see a fully configured document.
        self._init_plugins(plugins)

    # ---------- document replacement ----------

    def set_source(
        self,
        source: SourceType,
        *,
        apply_styles: bool = True,
    ) -> 'Report':
        """Replace the document with the contents of a .docx file.

        The current document is discarded. Counters for bookmarks,
        formulas and the last table are reset.

        Args:
            source: path to a .docx file, or an already-opened
                Document.
            apply_styles: if True (default), the Report's styles are
                applied to the new document so that user content
                added later has the expected look. Set to False to
                keep the source's styles completely untouched.

        Returns:
            self, for chaining.
        """
        return self.set_document(
            _load_source(source), apply_styles=apply_styles,
        )

    def set_document(
        self,
        doc: DocxDocument,
        *,
        apply_styles: bool = True,
    ) -> 'Report':
        """Replace the underlying Document object.

        Args:
            doc: a python-docx Document to install.
            apply_styles: if True (default), the Report's styles are
                applied to the new document.

        Returns:
            self, for chaining.
        """
        self.doc = doc
        if apply_styles:
            apply(self.doc, self.config)

        # Counters and references tied to the previous document are
        # no longer valid. Reset them so subsequent operations start
        # cleanly on the new document.
        self._bookmark_counter = 0
        self._formula_counter = 0
        self._last_table = None
        self._last_table_style = None
        return self

    # ---------- runtime configuration ----------

    def set_config(self, config: StylesConfig) -> None:
        """Replace the config and immediately re-apply styles.

        Existing content keeps its paragraph-level overrides (align
        passed to a specific p/h1 call). Only the underlying Word
        styles — Normal, Heading 1, ReportCode, ... — are re-derived
        from the new config.
        """
        self.config = config
        self.apply_styles()

    def apply_styles(self) -> None:
        """Re-apply the current config to document styles."""
        apply(self.doc, self.config)

    def set_metadata(self, metadata: DocumentMetadata) -> None:
        """Replace metadata. Applied to core_properties at save()."""
        self.metadata = metadata

    def apply_metadata(self) -> None:
        """Apply current metadata to core_properties now.

        Normally not needed: save() calls this automatically. Use it
        only if you need to inspect core_properties before saving.
        """
        apply_metadata_to_doc(self.doc, self.metadata)

    # ---------- accessors ----------

    def style(self, name: str):
        """Direct access to a python-docx style object."""
        return self.doc.styles[name]

    # ---------- lifecycle ----------

    def save(self, path: str) -> None:
        """Write the document, running plugin save hooks around it.

        Metadata is re-applied right before the write so that any
        runtime changes to self.metadata are picked up. Plugin
        before_save runs first, so plugins can still modify metadata
        or content before the final sync.
        """
        self._plugins_before_save(path)
        apply_metadata_to_doc(self.doc, self.metadata)
        self.doc.save(path)
        self._plugins_after_save(path)