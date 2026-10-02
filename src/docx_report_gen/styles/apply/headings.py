"""Apply Heading 1..N styles."""
from docx import Document

from ..config import StylesConfig
from ..resolvers import resolve_heading
from ..utils import apply_font


def apply_headings(doc: Document, config: StylesConfig) -> None:
    for level in range(1, len(config.heading_sizes) + 1):
        resolved = resolve_heading(config, level)
        apply_font(
            doc.styles[f'Heading {level}'],
            resolved,
            default_font=config.font,
        )