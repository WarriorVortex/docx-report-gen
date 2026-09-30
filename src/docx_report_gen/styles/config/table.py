"""Table style dataclass."""
from dataclasses import dataclass
from typing import Optional


@dataclass
class TableStyle:
    """Style for tables created by Report.table().

    `align` is the default alignment applied to cell paragraphs.
    `col_widths` — widths in centimeters, one per column, or a single
    number applied to every column.
    `col_aligns` — alignment per column; overrides `align`.
    `header_align` — alignment for the header row; overrides per-column
    settings when the header row is rendered.
    """
    align: Optional[str] = None
    col_widths: Optional[tuple[float, ...]] = None
    col_aligns: Optional[tuple[str, ...]] = None
    header_align: Optional[str] = None