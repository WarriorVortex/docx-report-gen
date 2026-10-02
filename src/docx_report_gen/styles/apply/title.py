"""Apply the Title (level 0) style."""
from ...docx import DocxDocument
from ..config import StylesConfig
from ..resolvers import resolve_title
from ..utils import apply_font, get_paragraph_style


def apply_title(doc: DocxDocument, config: StylesConfig) -> None:
    resolved = resolve_title(config)
    apply_font(
        get_paragraph_style(doc, 'Title'),
        resolved,
        default_font=config.font,
    )