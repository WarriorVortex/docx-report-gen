"""Session state for the writer singleton.

Holds the only mutable module-level variable in the writer package:
the current Report. Every other submodule reads it through `current()`
or mutates it through `new`, `attach`, `detach`, `reset`, `close`.
"""
from typing import Optional

from ..metadata import DocumentMetadata
from ..plugins import Plugin
from ..report import Report
from ..styles import StylesConfig


_current: Optional[Report] = None


def has_session() -> bool:
    """Return True if a Report exists in the current session."""
    return _current is not None


def current() -> Report:
    """Return the current Report, creating one on the first call.

    Lazy creation keeps `import docx_report_gen.writer` side-effect
    free: no document is constructed until the first write.
    """
    global _current
    if _current is None:
        _current = Report()
    return _current


def new(
    config: Optional[StylesConfig] = None,
    metadata: Optional[DocumentMetadata] = None,
    plugins: Optional[list[Plugin]] = None,
) -> Report:
    """Reset the session and create a fresh Report.

    Everything written before this call is discarded. The next
    block-level call operates on the new document.

    Args:
        config: StylesConfig for the new Report.
        metadata: DocumentMetadata for the new Report.
        plugins: additional plugins attached to this Report only.

    Returns:
        The newly created Report.
    """
    global _current
    _current = Report(
        config=config, metadata=metadata, plugins=plugins,
    )
    return _current


def attach(report: Report) -> Report:
    """Attach an existing Report as the current singleton.

    Replaces any active session without calling close() on it. Call
    close() or detach() first if teardown is required.

    Raises:
        TypeError: `report` is not a Report instance.
    """
    global _current
    if not isinstance(report, Report):
        raise TypeError(
            f'attach() expects a Report instance, '
            f'got {type(report).__name__}'
        )
    _current = report
    return report


def detach() -> Optional[Report]:
    """Detach and return the current Report.

    The Report is not closed — ownership returns to the caller.
    """
    global _current
    report = _current
    _current = None
    return report


def reset() -> None:
    """Drop the current Report without running plugin close hooks."""
    global _current
    _current = None


def close() -> None:
    """Run plugin close hooks on the current Report, then drop it.

    Idempotent — a second call with no active session does nothing.
    """
    global _current
    if _current is not None:
        _current.close()
        _current = None