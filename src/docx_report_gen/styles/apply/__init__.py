"""Apply StylesConfig to a python-docx Document."""
from ..config import StylesConfig
from ..._docx import DocumentProtocol
from .captions import apply_captions
from .code import apply_code
from .headings import apply_headings
from .lists import apply_lists
from .normal import apply_normal
from .page import apply_margins
from .quote import apply_quote
from .title import apply_title


def apply(doc: DocumentProtocol, config: StylesConfig) -> None:
    """Apply a StylesConfig to every relevant style of the document."""
    apply_normal(doc, config)
    apply_title(doc, config)
    apply_headings(doc, config)
    apply_lists(doc, config)
    apply_code(doc, config)
    apply_quote(doc, config)
    apply_captions(doc, config)
    apply_margins(doc, config)


__all__ = ['apply']