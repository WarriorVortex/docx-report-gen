"""Apply page-level settings (margins)."""
from docx.shared import Cm

from ...docx import DocxDocument
from ..config import StylesConfig


def apply_margins(doc: DocxDocument, config: StylesConfig) -> None:
    if not config.margins:
        return
    top, right, bottom, left = config.margins
    for section in doc.sections:
        section.top_margin = Cm(top)
        section.right_margin = Cm(right)
        section.bottom_margin = Cm(bottom)
        section.left_margin = Cm(left)