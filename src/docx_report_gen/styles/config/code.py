"""Code block style dataclass."""
from dataclasses import dataclass
from typing import Optional

from .layout import LayoutStyle
from .types import HexColor, RGB


@dataclass
class CodeStyle(LayoutStyle):
    """Style for monospace code blocks.

    `background` is a hex color without '#' (e.g. 'F5F5F5').

    To disable shading entirely, pass an empty string:

        CodeStyle(background='')

    Do not use `None` for that: in the three-level resolve chain, None
    means 'not set at this level, try the next source'. A CodeStyle
    with background=None leaves the default ('F5F5F5') in effect.
    Empty string is a valid, falsy value that skips the shading step
    in mixins/code.py and results in no background.
    """
    font: Optional[str] = 'Consolas'
    size: Optional[int] = 10
    color: Optional[RGB] = (32, 32, 32)
    background: Optional[HexColor] = 'F5F5F5'