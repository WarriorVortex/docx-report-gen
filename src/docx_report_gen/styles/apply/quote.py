"""Apply block quote style."""
from docx import Document
from docx.shared import Cm

from ..config import StylesConfig
from ..constants import QUOTE_STYLE_NAME
from ..resolvers import resolve_quote
from ..utils import apply_font, ensure_style


def apply_quote(doc: Document, config: StylesConfig) -> None:
    resolved = resolve_quote(config)
    style = ensure_style(doc, QUOTE_STYLE_NAME)
    apply_font(style, resolved, default_font=config.font)
    if resolved.indent is not None:
        style.paragraph_format.left_indent = Cm(resolved.indent)