"""Apply list styles."""
from docx import Document
from docx.shared import Cm

from ..config import StylesConfig
from ..constants import LIST_BULLET_STYLES, LIST_NUMBER_STYLES
from ..resolvers import resolve_list
from ..utils import apply_font, ensure_style


def apply_lists(doc: Document, config: StylesConfig) -> None:
    resolved = resolve_list(config)
    for name in (*LIST_BULLET_STYLES, *LIST_NUMBER_STYLES):
        try:
            style = doc.styles[name]
        except KeyError:
            continue
        apply_font(style, resolved, default_font=config.font)
        if resolved.indent is not None:
            style.paragraph_format.left_indent = Cm(resolved.indent)