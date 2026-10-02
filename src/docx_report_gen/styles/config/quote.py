"""Block quote style dataclass."""
from dataclasses import dataclass
from typing import Optional

from .layout import LayoutStyle
from .types import RGB


@dataclass
class QuoteStyle(LayoutStyle):
    """Style for block quotes."""
    font: Optional[str] = None
    size: Optional[int] = None
    color: Optional[RGB] = None
    italic: Optional[bool] = True