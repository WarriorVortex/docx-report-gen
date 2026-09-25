"""Apply caption styles (tables, images)."""
from docx import Document

from ..config import CaptionStyle, StylesConfig
from ..constants import (
    ALIGN, CAPTION_STYLE_NAME, IMAGE_CAPTION_STYLE_NAME,
)
from ..utils import apply_font, ensure_style


def _apply_caption_style(doc: Document, cs: CaptionStyle,
                         style_name: str, default_font: str) -> None:
    apply_font(
        ensure_style(doc, style_name),
        font=cs.font, size=cs.size, bold=cs.bold,
        italic=cs.italic, color=cs.color, align=cs.align,
        default_font=default_font, align_map=ALIGN,
    )


def apply_captions(doc: Document, config: StylesConfig) -> None:
    _apply_caption_style(
        doc, config.caption, CAPTION_STYLE_NAME, config.font,
    )
    _apply_caption_style(
        doc, config.image_caption, IMAGE_CAPTION_STYLE_NAME, config.font,
    )