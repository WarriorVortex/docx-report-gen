"""Heading methods mixin."""
from ..styles import ALIGN, resolve_heading, resolve_title
from ._base import DocMixin


class HeadingMixin(DocMixin):
    """Adds title() and h1()..h6() to Report."""

    def _add_heading(self, level, text, align):
        local = {'align': align}
        if level == 0:
            resolved = resolve_title(self.config, local)
        else:
            resolved = resolve_heading(self.config, level, local)
        para = self.doc.add_heading(text, level=level)
        para.alignment = ALIGN[resolved.align]
        return self

    def title(self, text, align=None):
        return self._add_heading(0, text, align)

    def h1(self, text, align=None): return self._add_heading(1, text, align)
    def h2(self, text, align=None): return self._add_heading(2, text, align)
    def h3(self, text, align=None): return self._add_heading(3, text, align)
    def h4(self, text, align=None): return self._add_heading(4, text, align)
    def h5(self, text, align=None): return self._add_heading(5, text, align)
    def h6(self, text, align=None): return self._add_heading(6, text, align)