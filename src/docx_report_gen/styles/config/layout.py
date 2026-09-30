"""Shared layout properties for paragraph-like style dataclasses."""
from dataclasses import dataclass
from typing import Optional


@dataclass
class LayoutStyle:
    """Layout properties common to paragraphs, code and quotes.

    All fields are optional. `None` means 'try the next source in
    the resolve chain'. Units:

        line_spacing       — multiplier (1.0 = single, 1.5 = one-and-half)
        space_before/after — points
        first_line_indent  — centimeters
        left_indent        — centimeters
    """
    align: Optional[str] = None
    line_spacing: Optional[float] = None
    space_before: Optional[int] = None
    space_after: Optional[int] = None
    first_line_indent: Optional[float] = None
    left_indent: Optional[float] = None