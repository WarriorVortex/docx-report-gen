"""Apply Heading 1..N styles."""
from ..._docx import DocxDocument
from ..config import StylesConfig
from ..resolvers import resolve_heading
from ..utils import apply_font, get_paragraph_style


def apply_headings(doc: DocxDocument, config: StylesConfig) -> None:
    for level in range(1, len(config.heading_sizes) + 1):
        resolved = resolve_heading(config, level)
        apply_font(
            get_paragraph_style(doc, f'Heading {level}'),
            resolved,
            default_font=config.font,
        )