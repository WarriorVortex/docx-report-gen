"""Apply the base ('Normal') paragraph style."""
from docx.shared import Pt, RGBColor

from ..._docx import DocumentProtocol
from ..config import StylesConfig
from ..utils import get_paragraph_style


def apply_normal(doc: DocumentProtocol, config: StylesConfig) -> None:
    normal = get_paragraph_style(doc, 'Normal')
    normal.font.name = config.font
    normal.font.size = Pt(config.size)
    normal.font.color.rgb = RGBColor(*config.color)