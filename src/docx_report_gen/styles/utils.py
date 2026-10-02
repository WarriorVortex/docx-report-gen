"""Generic style utilities."""
from dataclasses import fields
from typing import Any, Optional, Type, TypeVar, cast

from docx.enum.style import WD_STYLE_TYPE
from docx.shared import Pt, RGBColor
from docx.styles.style import ParagraphStyle

from ..docx import DocxDocument
from .constants import ALIGN


T = TypeVar('T')


def resolve(cls: Type[T], *sources: Any) -> T:
    """Return a fully-resolved instance of `cls`.

    For every field of `cls`, the first source providing a non-None
    value wins. Sources are checked left-to-right and may be:

      - an instance of `cls` (or any object with matching attributes)
      - a dict with field names as keys
      - None (skipped)

    Attributes missing on a source are skipped. When no source sets a
    field, the dataclass's own declared default is used. Enum-like
    fields (currently `align`) are validated and raise ValueError on
    an unknown value.
    """
    resolved: dict[str, Any] = {}
    # dataclasses.fields() is typed against DataclassInstance, which
    # is not expressible via TypeVar. mypy's own recommendation is to
    # silence the argument check here; the runtime contract (cls is a
    # dataclass class) is upheld by every call site in this package.
    for f in fields(cls):  # type: ignore[arg-type]
        for src in sources:
            if src is None:
                continue
            if isinstance(src, dict):
                value = src.get(f.name)
            else:
                value = getattr(src, f.name, None)
            if value is not None:
                if f.name == 'align' and value not in ALIGN:
                    allowed = sorted(k for k in ALIGN if k is not None)
                    raise ValueError(
                        f"invalid value for 'align' in {cls.__name__}: "
                        f"{value!r}; expected one of {allowed}"
                    )
                resolved[f.name] = value
                break
    return cls(**resolved)


def get_paragraph_style(doc: DocxDocument,
                        name: str) -> ParagraphStyle:
    """Return a style by name, typed as ParagraphStyle.

    Raises KeyError if the style does not exist. Use
    find_paragraph_style for a non-raising variant.
    """
    return cast(ParagraphStyle, doc.styles[name])


def find_paragraph_style(doc: DocxDocument,
                         name: str) -> Optional[ParagraphStyle]:
    """Return a paragraph style by name, or None if not present."""
    try:
        return cast(ParagraphStyle, doc.styles[name])
    except KeyError:
        return None


def ensure_style(doc: DocxDocument, name: str) -> ParagraphStyle:
    """Return an existing paragraph style or create a new one."""
    try:
        return cast(ParagraphStyle, doc.styles[name])
    except KeyError:
        return cast(
            ParagraphStyle,
            doc.styles.add_style(name, WD_STYLE_TYPE.PARAGRAPH),
        )


def apply_font(style: ParagraphStyle,
               resolved: object,
               default_font: str = 'Times New Roman') -> None:
    """Apply font properties of a resolved style to a Word style object.

    `resolved` is any style dataclass — HeadingStyle, CaptionStyle,
    CodeStyle, etc. Attributes are read defensively via getattr, so
    missing fields are silently skipped.
    """
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


__all__ = [
    'resolve',
    'apply_font',
    'ensure_style',
    'get_paragraph_style',
    'find_paragraph_style',
]