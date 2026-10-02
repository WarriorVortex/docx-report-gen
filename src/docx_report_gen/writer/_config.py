"""Accessors for config, metadata and python-docx styles."""
from typing import Any

from ..styles import StylesConfig

from ..metadata import DocumentMetadata
from ._state import current


def config() -> StylesConfig:
    """Return the current Report's StylesConfig."""
    return current().config


def set_config(new_config: StylesConfig) -> None:
    """Replace the current Report's StylesConfig.

    Does not re-apply styles to the document — affects only future
    style resolution. To restyle retroactively, mutate the desired
    style directly via `style(name)`.
    """
    current().config = new_config


def metadata() -> DocumentMetadata:
    """Return the current Report's DocumentMetadata."""
    return current().metadata


def set_metadata(new_metadata: DocumentMetadata) -> None:
    """Replace the current Report's DocumentMetadata.

    The change is written to core properties on save() only if you
    also run apply_metadata explicitly. See metadata.apply for details.
    """
    current().metadata = new_metadata


def style(name: str) -> Any:
    """Access a python-docx style object from the current document."""
    return current().style(name)