"""Image style dataclass."""
from dataclasses import dataclass
from typing import Optional


@dataclass
class ImageStyle:
    """Layout for images inserted via Report.img().

    `width` is in centimeters. `align=None` means 'inherit from
    StylesConfig.align'.
    """
    align: Optional[str] = None
    width: Optional[float] = None