"""Utility helpers shared by the style application steps."""
from docx import Document
from docx.enum.style import WD_STYLE_TYPE
from docx.shared import Pt, RGBColor

from .config import HeadingStyle


def merge(base: HeadingStyle, override: HeadingStyle) -> HeadingStyle:
    """Return a new HeadingStyle with `override` fields taking precedence.

    Fields left as None in `override` are taken from `base`.
    """
    def pick(name):
        value = getattr(override, name)
        return value if value is not None else getattr(base, name)

    return HeadingStyle(
        font=pick('font'),
        size=pick('size'),
        bold=pick('bold'),
        italic=pick('italic'),
        color=pick('color'),
        align=pick('align'),
    )


def apply_font(style, *, font, size, bold, italic, color, align,
               default_font, align_map):
    """Apply font and paragraph properties to a Word style object.

    Args:
        style: a python-docx style object to modify.
        font: font name; falls back to `default_font` if None.
        size: size in points, or None to leave unchanged.
        bold, italic: True/False to set, None to leave unchanged.
        color: (r, g, b) tuple, or None to leave unchanged.
        align: string key into `align_map`, or None to leave unchanged.
        default_font: fallback font name when `font` is None.
        align_map: mapping of align-name -> WD_ALIGN_PARAGRAPH value.
    """
    style.font.name = font or default_font
    if size is not None:
        style.font.size = Pt(size)
    if bold is not None:
        style.font.bold = bold
    if italic is not None:
        style.font.italic = italic
    if color is not None:
        style.font.color.rgb = RGBColor(*color)
    if align is not None:
        style.paragraph_format.alignment = align_map[align]


def ensure_style(doc: Document, name: str):
    """Return an existing style by name or create a new paragraph style."""
    try:
        return doc.styles[name]
    except KeyError:
        return doc.styles.add_style(name, WD_STYLE_TYPE.PARAGRAPH)