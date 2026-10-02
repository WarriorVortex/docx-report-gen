"""Generic style utilities."""
from dataclasses import fields

from docx.enum.style import WD_STYLE_TYPE
from docx.shared import Pt, RGBColor


def resolve(cls, *sources):
    """Return a fully-resolved instance of `cls`.

    For every field of `cls`, the first source providing a non-None
    value wins. Sources are checked left-to-right and may be:
      - an instance of `cls` (or any object with matching attributes)
      - a dict with field names as keys
      - None (skipped)

    Attributes missing on a source are skipped. When no source sets a
    field, the dataclass's own declared default is used.

    Args:
        cls: style dataclass (HeadingStyle, CaptionStyle, ...).
        *sources: sources in priority order, typically ending with the
            global StylesConfig to supply font/size/color/align.

    Returns:
        An instance of `cls` with every field resolved.
    """
    resolved = {}
    for f in fields(cls):
        for src in sources:
            if src is None:
                continue
            if isinstance(src, dict):
                value = src.get(f.name)
            else:
                value = getattr(src, f.name, None)
            if value is not None:
                resolved[f.name] = value
                break
    return cls(**resolved)


def apply_font(style, resolved, default_font='Times New Roman'):
    """Apply font properties of a resolved style to a Word style object."""
    style.font.name = getattr(resolved, 'font', None) or default_font
    size = getattr(resolved, 'size', None)
    if size is not None:
        style.font.size = Pt(size)
    bold = getattr(resolved, 'bold', None)
    if bold is not None:
        style.font.bold = bold
    italic = getattr(resolved, 'italic', None)
    if italic is not None:
        style.font.italic = italic
    color = getattr(resolved, 'color', None)
    if color is not None:
        style.font.color.rgb = RGBColor(*color)


def ensure_style(doc, name):
    """Return an existing style by name or create a new paragraph style."""
    try:
        return doc.styles[name]
    except KeyError:
        return doc.styles.add_style(name, WD_STYLE_TYPE.PARAGRAPH)