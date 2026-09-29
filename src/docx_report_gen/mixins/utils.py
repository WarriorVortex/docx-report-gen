"""Shared utilities for Report mixins."""
from docx import Document
from docx.text.paragraph import Paragraph

from ..styles import ALIGN


def render_caption(doc: Document, caption_style, style_name: str,
                   n: int, caption: str) -> Paragraph:
    """Add a numbered caption paragraph and return it.

    `caption_style` must be fully resolved — prefix, template and
    align are used as-is.
    """
    text = caption_style.template.format(
        prefix=caption_style.prefix, n=n, caption=caption,
    )
    para = doc.add_paragraph(style=style_name)
    para.add_run(text)
    para.alignment = ALIGN[caption_style.align]
    return para