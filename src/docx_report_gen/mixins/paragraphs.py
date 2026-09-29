"""Paragraph and block formula mixin."""
import math2docx

from ..inline import Inline
from ..styles import ALIGN, resolve_formula, resolve_paragraph
from ._base import DocMixin


class ParagraphMixin(DocMixin):
    """Adds p() and block f() to Report."""

    def p(self, *parts, align=None):
        """Paragraph from strings and inline nodes (b, i, f)."""
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

    def f(self, latex, align=None):
        """Standalone block formula on its own paragraph."""
        resolved = resolve_formula(self.config, {'align': align})
        para = self.doc.add_paragraph()
        para.alignment = ALIGN[resolved.align]
        math2docx.add_math(para, latex)
        return self