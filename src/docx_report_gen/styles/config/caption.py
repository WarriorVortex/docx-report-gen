"""Caption style dataclass."""
from dataclasses import dataclass
from typing import Optional

from .types import RGB


@dataclass
class CaptionStyle:
    """Style and numbering format for table captions.

    The `template` is rendered with str.format() and may use three
    placeholders: {prefix}, {n}, {caption}. Examples:

        '{prefix} {n} — {caption}'   -> 'Таблица 1 — Результаты'
        'Table {n}: {caption}'        -> 'Table 1: Results'
        'Табл. {n}. {caption}'        -> 'Табл. 1. Результаты'
        '{prefix} {n}'                -> 'Таблица 1'
    """
    prefix: str = 'Таблица'
    template: str = '{prefix} {n} — {caption}'
    align: str = 'left'
    font: Optional[str] = None
    size: Optional[int] = None
    bold: Optional[bool] = None
    italic: Optional[bool] = None
    color: Optional[RGB] = None