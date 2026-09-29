"""Paragraph, block formula and quote mixin."""
from docx.enum.text import WD_TAB_ALIGNMENT

import math2docx

from .._xml import add_page_number  # noqa: F401 (kept for future use)
from ..inline import Inline
from ..styles import (
    ALIGN, QUOTE_STYLE_NAME,
    resolve_formula, resolve_paragraph, resolve_quote,
)
from ._base import DocMixin


class ParagraphMixin(DocMixin):
    """Adds p(), f() and quote() to Report."""

    _formula_counter = 0

    def p(self, *parts, align=None):
        """Paragraph from strings and inline nodes (b, i, f, link)."""
        resolved = resolve_paragraph(self.config, {'align': align})
        para = self.doc.add_paragraph()
        para.alignment = ALIGN[resolved.align]
        for part in parts:
            if isinstance(part, str):
                para.add_run(part)
            elif isinstance(part, Inline):
                part.render(para)
            else:
                raise TypeError(
                    f'p() accepts str or inline nodes, '
                    f'got {type(part).__name__}'
                )
        return self

    def f(self, latex, align=None, number=False):
        """Standalone block formula.

        Args:
            latex: formula in LaTeX.
            align: alignment override when `number` is False.
            number: if True, the formula is centered and its number
                `(N)` is right-aligned on the same line. Word will
                update the layout via tab stops.
        """
        para = self.doc.add_paragraph()
        if number:
            self._formula_counter += 1
            self._setup_formula_tabs(para)
            para.add_run('\t')
            math2docx.add_math(para, latex)
            para.add_run('\t')
            para.add_run(f'({self._formula_counter})')
        else:
            resolved = resolve_formula(self.config, {'align': align})
            para.alignment = ALIGN[resolved.align]
            math2docx.add_math(para, latex)
        return self

    def quote(self, *parts, align=None):
        """Block quote paragraph."""
        resolved = resolve_quote(self.config, {'align': align})
        para = self.doc.add_paragraph(style=QUOTE_STYLE_NAME)
        para.alignment = ALIGN[resolved.align]
        for part in parts:
            if isinstance(part, str):
                para.add_run(part)
            elif isinstance(part, Inline):
                part.render(para)
            else:
                raise TypeError(
                    f'quote() accepts str or inline nodes, '
                    f'got {type(part).__name__}'
                )
        return self

    def _setup_formula_tabs(self, para):
        """Add center + right tab stops across the content width."""
        section = self.doc.sections[0]
        content = (
            section.page_width
            - section.left_margin
            - section.right_margin
        )
        para.paragraph_format.tab_stops.add_tab_stop(
            content / 2, WD_TAB_ALIGNMENT.CENTER,
        )
        para.paragraph_format.tab_stops.add_tab_stop(
            content, WD_TAB_ALIGNMENT.RIGHT,
        )