"""List style dataclass."""
from dataclasses import dataclass
from typing import Optional

from .layout import LayoutStyle
from .types import RGB


@dataclass
class ListStyle(LayoutStyle):
    """Style for bullet and numbered lists.

    Inherits layout fields from LayoutStyle — the alignment, indents
    and spacing apply to the base (first) level of the list. Nested
    levels follow Word's built-in list styles and are spaced by Word.

    `left_indent` is applied to the paragraph format of each list
    style (List Bullet, List Number and their level 2/3 variants).
    """
    font: Optional[str] = None
    size: Optional[int] = None
    color: Optional[RGB] = None