"""Apply list styles."""
from docx.shared import Cm

from ..._docx import DocumentProtocol
from ..config import StylesConfig
from ..constants import LIST_BULLET_STYLES, LIST_NUMBER_STYLES
from ..resolvers import resolve_list
from ..utils import apply_font, find_paragraph_style


def apply_lists(doc: DocumentProtocol, config: StylesConfig) -> None:
    resolved = resolve_list(config)
    for name in (*LIST_BULLET_STYLES, *LIST_NUMBER_STYLES):
        style = find_paragraph_style(doc, name)
        if style is None:
            continue
        apply_font(style, resolved, default_font=config.font)
        if resolved.indent is not None:
            style.paragraph_format.left_indent = Cm(resolved.indent)