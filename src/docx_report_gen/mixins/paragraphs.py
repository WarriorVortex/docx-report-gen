"""Paragraph and block formula mixin."""
import math2docx

from ..inline import Inline
from ..styles import ALIGN
from ._base import DocMixin


class ParagraphMixin(DocMixin):
    """Adds p() and block f() to Report."""

    def p(self, *parts: str | Inline, align: str = 'justify'):
        """Paragraph from strings and inline nodes (b, i, f)."""
        para = self.doc.add_paragraph()
        para.alignment = ALIGN[align]
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

    def f(self, latex: str, align: str = 'center'):
        """Standalone block formula on its own paragraph."""
        para = self.doc.add_paragraph()
        para.alignment = ALIGN[align]
        math2docx.add_math(para, latex)
        return self