"""Apply caption styles (tables, images)."""
from ...docx import DocxDocument
from ..config import StylesConfig
from ..constants import CAPTION_STYLE_NAME, IMAGE_CAPTION_STYLE_NAME
from ..resolvers import resolve_caption, resolve_image_caption
from ..utils import apply_font, ensure_style


def apply_captions(doc: DocxDocument, config: StylesConfig) -> None:
    apply_font(
        ensure_style(doc, CAPTION_STYLE_NAME),
        resolve_caption(config),
        default_font=config.font,
    )
    apply_font(
        ensure_style(doc, IMAGE_CAPTION_STYLE_NAME),
        resolve_image_caption(config),
        default_font=config.font,
    )