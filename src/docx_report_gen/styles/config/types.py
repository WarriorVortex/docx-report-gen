"""Shared type aliases used across the package.

Kept in a dedicated module without imports from the package itself,
so every other module can depend on it without creating cycles.
Every alias carries an explicit TypeAlias marker so that type checkers
and IDEs treat it as a type, not as a plain value.
"""
from pathlib import Path
from typing import Literal, Union

from typing_extensions import TypeAlias


RGB: TypeAlias = tuple[int, int, int]
"""An (r, g, b) tuple, each component in 0..255."""

HexColor: TypeAlias = str
"""A hex color without '#', e.g. 'F5F5F5'."""

AlignLiteral: TypeAlias = Literal['left', 'center', 'right', 'justify']
"""Valid alignment names for paragraphs, headings, captions and tables."""

PathLike: TypeAlias = Union[str, Path]
"""Any value accepted where a filesystem path is expected."""

Margins: TypeAlias = tuple[float, float, float, float]
"""Page margins in centimeters: (top, right, bottom, left)."""