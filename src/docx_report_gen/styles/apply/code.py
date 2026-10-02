"""Apply code block style."""
from ..._docx import DocxDocument
from ..config import StylesConfig
from ..constants import CODE_STYLE_NAME
from ..resolvers import resolve_code
from ..utils import apply_font, ensure_style


def apply_code(doc: DocxDocument, config: StylesConfig) -> None:
    apply_font(
        ensure_style(doc, CODE_STYLE_NAME),
        resolve_code(config),
        default_font='Consolas',
    )