"""Heading style dataclass."""
from dataclasses import dataclass
from typing import Optional

from .types import RGB


@dataclass
class HeadingStyle:
    """Style for one heading level.

    Any field left as None means 'inherit the default from StylesConfig'.
    """
    font: Optional[str] = None
    size: Optional[int] = None
    bold: Optional[bool] = None
    italic: Optional[bool] = None
    color: Optional[RGB] = None
    align: Optional[str] = None