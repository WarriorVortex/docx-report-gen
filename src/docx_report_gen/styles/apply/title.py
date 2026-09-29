"""Apply the Title (level 0) style."""
from docx import Document

from ..config import StylesConfig
from ..resolvers import resolve_title
from ..utils import apply_font


def apply_title(doc: Document, config: StylesConfig) -> None:
    resolved = resolve_title(config)
    apply_font(doc.styles['Title'], resolved, default_font=config.font)