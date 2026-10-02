"""Paragraph, block formula and quote mixin."""
from docx.enum.text import WD_TAB_ALIGNMENT

import math2docx

from ..styles import (
    QUOTE_STYLE_NAME,
    resolve_formula, resolve_paragraph, resolve_quote,
)
from ._base import DocMixin
from .utils import apply_layout, check_align, check_parts


class ParagraphMixin(DocMixin):
    """Adds p(), f() and quote() to Report."""

    _formula_counter = 0

    def p(self, *parts, align=None, line_spacing=None,
          space_before=None, space_after=None, first_line_indent=None):
        """Paragraph from strings and inline nodes.

        Args:
            *parts: strings and inline nodes (b, i, u, s, sup, sub,
                color, highlight, f, link).
            align, line_spacing, space_before, space_after,
            first_line_indent: local layout overrides. None falls back
                to StylesConfig.paragraph, then to StylesConfig itself.
        """
        check_align(align, where='p')
        check_parts(parts, where='p')
        local = {
            'align': align,
            'line_spacing': line_spacing,
            'space_before': space_before,
            'space_after': space_after,
            'first_line_indent': first_line_indent,
        }
        resolved = resolve_paragraph(self.config, local)
        para = self.doc.add_paragraph()
        apply_layout(para, resolved)
        for part in parts:
            if isinstance(part, str):
                para.add_run(part)
            else:
                part.render(para)
        return self

    def f(self, latex, align=None, number=False):
        """Standalone block formula.

        Args:
            latex: formula in LaTeX.
            align: alignment override when `number` is False.
            number: if True, the formula is centered and its number
                `(N)` is right-aligned on the same line.
        """
        check_align(align, where='f')
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
            apply_layout(para, resolved)
            math2docx.add_math(para, latex)
        return self

    def quote(self, *parts, align=None, line_spacing=None,
              space_before=None, space_after=None,
              first_line_indent=None, left_indent=None):
        """Block quote paragraph."""
        check_align(align, where='quote')
        check_parts(parts, where='quote')
        local = {
            'align': align,
            'line_spacing': line_spacing,
            'space_before': space_before,
            'space_after': space_after,
            'first_line_indent': first_line_indent,
            'left_indent': left_indent,
        }
        resolved = resolve_quote(self.config, local)
        para = self.doc.add_paragraph(style=QUOTE_STYLE_NAME)
        apply_layout(para, resolved)
        for part in parts:
            if isinstance(part, str):
                para.add_run(part)
            else:
                part.render(para)
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