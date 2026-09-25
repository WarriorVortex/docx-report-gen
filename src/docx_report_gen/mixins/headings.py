"""Heading methods mixin."""
from ..styles import ALIGN
from ._base import DocMixin


class HeadingMixin(DocMixin):
    """Adds title() and h1()..h6() to Report."""

    def title(self, text: str, align: str = 'center'):
        self.doc.add_heading(text, level=0).alignment = ALIGN[align]
        return self

    def _heading(self, level: int, text: str, align: str | None = None):
        self.doc.add_heading(text, level=level).alignment = ALIGN[align]
        return self

    def h1(self, text: str, align: str | None = None): return self._heading(1, text, align)
    def h2(self, text: str, align: str | None = None): return self._heading(2, text, align)
    def h3(self, text: str, align: str | None = None): return self._heading(3, text, align)
    def h4(self, text: str, align: str | None = None): return self._heading(4, text, align)
    def h5(self, text: str, align: str | None = None): return self._heading(5, text, align)
    def h6(self, text: str, align: str | None = None): return self._heading(6, text, align)