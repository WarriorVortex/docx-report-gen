"""Apply the Title (level 0) style."""
from docx import Document

from ..config import HeadingStyle, StylesConfig
from ..constants import ALIGN
from ..utils import apply_font, merge


def apply_title(doc: Document, config: StylesConfig) -> None:
    title = merge(HeadingStyle(color=config.color), config.title)
    apply_font(
        doc.styles['Title'],
        font=title.font, size=title.size, bold=title.bold,
        italic=title.italic, color=title.color, align=title.align,
        default_font=config.font, align_map=ALIGN,
    )