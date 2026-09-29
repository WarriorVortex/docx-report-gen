"""Block quote style dataclass."""
from dataclasses import dataclass
from typing import Optional

from .types import RGB


@dataclass
class QuoteStyle:
    """Style for block quotes."""
    align: Optional[str] = None
    indent: Optional[float] = 1.0   # cm
    font: Optional[str] = None
    size: Optional[int] = None
    color: Optional[RGB] = None
    italic: Optional[bool] = True