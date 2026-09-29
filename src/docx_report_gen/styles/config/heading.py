"""Heading style dataclass."""
from dataclasses import dataclass
from typing import Optional

from .types import RGB


@dataclass
class HeadingStyle:
    """Style for one heading level.

    Any field left as None means 'not set here — try the next source
    in the resolve() chain'.
    """
    font: Optional[str] = None
    size: Optional[int] = None
    bold: Optional[bool] = None
    italic: Optional[bool] = None
    color: Optional[RGB] = None
    align: Optional[str] = None