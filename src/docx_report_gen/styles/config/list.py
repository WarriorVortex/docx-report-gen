"""List style dataclass."""
from dataclasses import dataclass
from typing import Optional

from .types import RGB


@dataclass
class ListStyle:
    """Style for bullet and numbered lists.

    `indent` is the left indent in centimeters for the first level.
    Word's built-in list styles handle nesting automatically, so
    `indent` applies to the base style only.
    """
    align: Optional[str] = None
    indent: Optional[float] = None
    font: Optional[str] = None
    size: Optional[int] = None
    color: Optional[RGB] = None