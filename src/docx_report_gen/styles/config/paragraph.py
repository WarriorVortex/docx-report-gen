"""Paragraph style dataclass."""
from dataclasses import dataclass

from .layout import LayoutStyle


@dataclass
class ParagraphStyle(LayoutStyle):
    """Layout for body paragraphs (Report.p) and formulas (Report.f)."""
    pass