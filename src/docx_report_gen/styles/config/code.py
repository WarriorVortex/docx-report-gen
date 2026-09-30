"""Code block style dataclass."""
from dataclasses import dataclass
from typing import Optional

from .layout import LayoutStyle
from .types import RGB


@dataclass
class CodeStyle(LayoutStyle):
    """Style for monospace code blocks.

    `background` is a hex color without '#' (e.g. 'F5F5F5'), or None
    for no shading.
    """
    font: Optional[str] = 'Consolas'
    size: Optional[int] = 10
    color: Optional[RGB] = (32, 32, 32)
    background: Optional[str] = 'F5F5F5'