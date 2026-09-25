"""Apply Heading 1..N styles."""
from docx import Document

from ..config import HeadingStyle, StylesConfig
from ..constants import ALIGN
from ..utils import apply_font, merge


def apply_headings(doc: Document, config: StylesConfig) -> None:
    h = config.heading
    for level, size in enumerate(config.heading_sizes, start=1):
        base = HeadingStyle(
            font=h.font, size=size, bold=h.bold,
            italic=h.italic, color=h.color, align=h.align,
        )
        override = config.heading_overrides.get(level, HeadingStyle())
        resolved = merge(base, override)
        apply_font(
            doc.styles[f'Heading {level}'],
            font=resolved.font, size=resolved.size, bold=resolved.bold,
            italic=resolved.italic, color=resolved.color,
            align=resolved.align,
            default_font=config.font, align_map=ALIGN,
        )