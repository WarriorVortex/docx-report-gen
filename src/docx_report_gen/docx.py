"""Public re-exports from python-docx.

Users of docx-report-gen may need the same primitives that python-docx
provides when they write plugins, custom inline nodes, or their own
mixins. Importing them from `docx` directly mixes two packages in user
code and makes it harder to swap the underlying library later.

This module is the single point where those primitives are re-exported
under the docx-report-gen namespace:

    from docx_report_gen import docx
    docx.DocxDocument
    docx.to_twips(1.25)            # 1.25 cm -> 709 twips
    docx.WD_COLOR_INDEX

or:

    from docx_report_gen.docx import DocxDocument, to_twips

The name `DocxDocument` is used for the class because `Document` also
names a factory function in python-docx's public API. The factory and
the class are distinct; the factory returns instances of the class.
Internal modules of this package use `DocxDocument` for annotations.
"""
from typing import Union

from docx.document import Document as DocxDocument
from docx.table import Table
from docx.text.paragraph import Paragraph
from docx.text.run import Run
from docx.shared import Cm, Emu, Inches, Length, Mm, Pt, RGBColor
from docx.enum.text import (
    WD_ALIGN_PARAGRAPH,
    WD_BREAK_TYPE,
    WD_COLOR_INDEX,
    WD_LINE_SPACING,
    WD_TAB_ALIGNMENT,
    WD_UNDERLINE,
)


# A length value accepted by to_twips: a plain number or a python-docx
# Length object (which subclasses int and carries a unit).
LengthValue = Union[int, float, Length]


def to_twips(value: LengthValue, unit: str = 'cm') -> int:
    """Convert a length to twips (twentieths of a point).

    Twips are the unit Word uses internally for indents, spacing and
    tab stops. python-docx converts on assignment using its own
    rounding; this helper exposes the same conversion, so tests and
    plugins can produce the exact integer that ends up in the XML.

    Args:
        value: a number, or a python-docx Length instance. When a
            Length is passed, `unit` is ignored and the value is
            used as-is.
        unit: one of 'cm', 'mm', 'in', 'pt'. Defaults to 'cm'.

    Returns:
        The length in twips, as an int.

    Raises:
        ValueError: unknown unit.
    """
    # python-docx's .twips attribute is not type-annotated; int() forces
    # the value into the declared return type and guards against a
    # future change that would return something non-int.
    if isinstance(value, Length):
        return int(value.twips)
    if unit == 'cm':
        return int(Cm(value).twips)
    if unit == 'mm':
        return int(Mm(value).twips)
    if unit == 'in':
        return int(Inches(value).twips)
    if unit == 'pt':
        return int(Pt(value).twips)
    raise ValueError(
        f"unknown unit: {unit!r}; expected 'cm', 'mm', 'in' or 'pt'"
    )


__all__ = [
    # core types
    'DocxDocument',
    'Paragraph',
    'Run',
    'Table',
    # length helpers
    'Cm',
    'Emu',
    'Inches',
    'Length',
    'LengthValue',
    'Mm',
    'Pt',
    'to_twips',
    # colors
    'RGBColor',
    # enums
    'WD_ALIGN_PARAGRAPH',
    'WD_BREAK_TYPE',
    'WD_COLOR_INDEX',
    'WD_LINE_SPACING',
    'WD_TAB_ALIGNMENT',
    'WD_UNDERLINE',
]