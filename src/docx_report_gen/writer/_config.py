"""Accessors for config, metadata and python-docx styles."""
from typing import Any

from ..metadata import DocumentMetadata
from ..styles import StylesConfig
from ._state import current


def config() -> StylesConfig:
    """Return the current Report's StylesConfig."""
    return current().config


def set_config(new_config: StylesConfig) -> None:
    """Replace the current Report's StylesConfig and re-apply styles.

    Underlying Word styles (Normal, Heading 1, ReportCode, ...) are
    re-derived from the new config. Paragraph-level overrides made by
    individual calls — e.g. h1('X', align='center') — are preserved.
    """
    current().set_config(new_config)


def apply_styles() -> None:
    """Re-apply the current config to document styles.

    Use after mutating config in place:

        writer.config().heading.align = 'center'
        writer.apply_styles()
    """
    current().apply_styles()


def metadata() -> DocumentMetadata:
    """Return the current Report's DocumentMetadata."""
    return current().metadata


def set_metadata(new_metadata: DocumentMetadata) -> None:
    """Replace the current Report's DocumentMetadata.

    The change is written to core_properties automatically at save().
    To inspect core_properties before saving, call sync_metadata().
    """
    current().set_metadata(new_metadata)


def sync_metadata() -> None:
    """Apply current metadata to core_properties immediately.

    save() does this automatically. Call only if you need to inspect
    core_properties before the next save().
    """
    current().sync_metadata()


def style(name: str) -> Any:
    """Access a python-docx style object from the current document."""
    return current().style(name)