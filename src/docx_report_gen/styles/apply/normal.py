"""Apply the base ('Normal') paragraph style."""
from docx import Document
from docx.shared import Pt, RGBColor

from ..config import StylesConfig


def apply_normal(doc: Document, config: StylesConfig) -> None:
    normal = doc.styles['Normal']
    normal.font.name = config.font
    normal.font.size = Pt(config.size)
    normal.font.color.rgb = RGBColor(*config.color)