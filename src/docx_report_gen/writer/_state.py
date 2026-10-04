"""Session state for the writer singleton."""
from typing import Optional, Union
from pathlib import Path

from ..docx import DocxDocument
from ..metadata import DocumentMetadata
from ..plugins import Plugin
from ..report import Report
from ..styles import StylesConfig


SourceType = Union[str, Path, DocxDocument]

_current: Optional[Report] = None


def has_session() -> bool:
    """Return True if a Report exists in the current session."""
    return _current is not None


def current() -> Report:
    """Return the current Report, creating one on the first call."""
    global _current
    if _current is None:
        _current = Report()
    return _current


def new(
    config: Optional[StylesConfig] = None,
    metadata: Optional[DocumentMetadata] = None,
    plugins: Optional[list[Plugin]] = None,
    source: Optional[SourceType] = None,
) -> Report:
    """Reset the session and create a fresh Report.

    Args:
        config: StylesConfig for the new Report.
        metadata: DocumentMetadata for the new Report.
        plugins: additional plugins attached to this Report only.
        source: optional base document. A path to a .docx file, or an
            already-opened Document. When given, the file becomes the
            base of the Report; when None, an empty document is used.

    Returns:
        The newly created Report.
    """
    global _current
    _current = Report(
        config=config, metadata=metadata, plugins=plugins,
        source=source,
    )
    return _current


def set_source(
    source: SourceType,
    *,
    apply_styles: bool = True,
) -> Report:
    """Replace the current Report's document with a .docx file.

    Equivalent to `current().set_source(source)`. Creates a session
    if none exists.

    Returns:
        The current Report.
    """
    return current().set_source(source, apply_styles=apply_styles)


def set_document(
    doc: DocxDocument,
    *,
    apply_styles: bool = True,
) -> Report:
    """Replace the current Report's Document object.

    Equivalent to `current().set_document(doc)`. Creates a session
    if none exists.

    Returns:
        The current Report.
    """
    return current().set_document(doc, apply_styles=apply_styles)


def attach(report: Report) -> Report:
    """Attach an existing Report as the current singleton."""
    global _current
    if not isinstance(report, Report):
        raise TypeError(
            f'attach() expects a Report instance, '
            f'got {type(report).__name__}'
        )
    _current = report
    return report


def detach() -> Optional[Report]:
    """Detach and return the current Report."""
    global _current
    report = _current
    _current = None
    return report


def reset() -> None:
    """Drop the current Report without running plugin close hooks."""
    global _current
    _current = None


def close() -> None:
    """Run plugin close hooks on the current Report, then drop it."""
    global _current
    if _current is not None:
        _current.close()
        _current = None