"""Paragraph style dataclass."""
from dataclasses import dataclass
from typing import Optional


@dataclass
class ParagraphStyle:
    """Layout for body paragraphs (Report.p) and block formulas (Report.f)."""
    align: Optional[str] = None