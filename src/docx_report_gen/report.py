"""Report class — assembles all mixins into a single builder."""
from typing import Optional, Any

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


class Report(HeadingMixin, ParagraphMixin, ListMixin, CodeMixin,
              TableMixin, ImageMixin, BookmarkMixin, TocMixin,
              LayoutMixin, PluginMixin):
    """Declarative docx report builder.

    Config and metadata can be set at construction time or changed
    later:

        r = Report(config=cfg, metadata=md)

        # Runtime replacement, styles re-applied immediately:
        r.set_config(other_cfg)

        # Runtime replacement, applied at next save():
        r.set_metadata(other_md)

        # In-place config mutation, opt-in re-apply:
        r.config.heading.align = 'center'
        r.apply_styles()

        # In-place metadata mutation, opt-in flush to core_properties:
        r.metadata.author = 'X'
        r.apply_metadata()

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
    ) -> None:
        self.config = config or StylesConfig()
        self.metadata = metadata or DocumentMetadata()
        self.doc = Document()

        # Cooperative init: stateful mixins set their private state
        # here. The MRO chain runs each __init__ exactly once.
        super().__init__()

        apply(self.doc, self.config)
        apply_metadata_to_doc(self.doc, self.metadata)

        # Plugins must see a fully configured document.
        self._init_plugins(plugins)

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
        """Re-apply the current config to document styles.

        Use after mutating config in place:

            r.config.heading.align = 'center'
            r.apply_styles()
        """
        apply(self.doc, self.config)

    def set_metadata(self, metadata: DocumentMetadata) -> None:
        """Replace metadata. Applied to core_properties at save().

        To make the change visible in core_properties immediately,
        call apply_metadata() afterwards.
        """
        self.metadata = metadata

    def apply_metadata(self) -> None:
        """Apply current metadata to core_properties now.

        Normally not needed: save() calls this automatically. Use it
        only if you need to inspect core_properties before saving,
        or to flush an in-place change to self.metadata.
        """
        apply_metadata_to_doc(self.doc, self.metadata)

    # ---------- accessors ----------

    def style(self, name: str) -> Any:
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