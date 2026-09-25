"""Shared utilities for Report mixins."""
from docx import Document
from docx.text.paragraph import Paragraph

from ..styles import ALIGN


def render_caption(doc: Document, caption_style, style_name: str,
                   n: int, caption: str) -> Paragraph:
    """Add a numbered caption paragraph and return it.

    Args:
        doc: document to append the caption to.
        caption_style: a CaptionStyle (prefix / template / alignment).
        style_name: name of the Word paragraph style to apply.
        n: caption number within its category.
        caption: caption text.
    """
    text = caption_style.template.format(
        prefix=caption_style.prefix, n=n, caption=caption,
    )
    para = doc.add_paragraph(style=style_name)
    para.add_run(text)
    para.alignment = ALIGN[caption_style.align]
    return para