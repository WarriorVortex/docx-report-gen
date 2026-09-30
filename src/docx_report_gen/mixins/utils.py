"""Shared utilities for Report mixins."""
from docx import Document
from docx.shared import Pt, Cm
from docx.text.paragraph import Paragraph

from ..styles import ALIGN


def check_align(value, where='method'):
    """Raise ValueError if `value` is not a valid alignment name.

    None is allowed and means 'use the resolved subconfig value'.
    """
    if value is None:
        return
    if value not in ALIGN:
        allowed = sorted(k for k in ALIGN if k is not None)
        raise ValueError(
            f"invalid align in {where}(): {value!r}; "
            f"expected one of {allowed}"
        )


def check_parts(parts, where='p'):
    """Raise TypeError on the first part that is not str or Inline."""
    from ..inline import Inline
    for part in parts:
        if not isinstance(part, (str, Inline)):
            raise TypeError(
                f"{where}() accepts str or inline nodes "
                f"(b, i, u, s, sup, sub, color, highlight, f, link); "
                f"got {type(part).__name__}"
            )


def apply_layout(para: Paragraph, resolved) -> None:
    """Apply resolved layout properties to a paragraph.

    Accepts any style object that exposes `align`, `line_spacing`,
    `space_before`, `space_after`, `first_line_indent`, `left_indent`.
    Missing attributes and None values are skipped silently, so the
    same helper works for ParagraphStyle, CodeStyle and QuoteStyle.
    """
    align = getattr(resolved, 'align', None)
    if align is not None:
        para.alignment = ALIGN[align]

    pf = para.paragraph_format

    line_spacing = getattr(resolved, 'line_spacing', None)
    if line_spacing is not None:
        pf.line_spacing = line_spacing

    space_before = getattr(resolved, 'space_before', None)
    if space_before is not None:
        pf.space_before = Pt(space_before)

    space_after = getattr(resolved, 'space_after', None)
    if space_after is not None:
        pf.space_after = Pt(space_after)

    first_line_indent = getattr(resolved, 'first_line_indent', None)
    if first_line_indent is not None:
        pf.first_line_indent = Cm(first_line_indent)

    left_indent = getattr(resolved, 'left_indent', None)
    if left_indent is not None:
        pf.left_indent = Cm(left_indent)


def render_caption(doc: Document, caption_style, style_name: str,
                   n: int, caption: str) -> Paragraph:
    """Add a numbered caption paragraph and return it."""
    text = caption_style.template.format(
        prefix=caption_style.prefix, n=n, caption=caption,
    )
    para = doc.add_paragraph(style=style_name)
    para.add_run(text)
    para.alignment = ALIGN[caption_style.align]
    return para