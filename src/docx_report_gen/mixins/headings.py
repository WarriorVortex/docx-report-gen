"""Heading methods mixin."""
from typing import Any, Optional

from ..styles import ALIGN, AlignLiteral, resolve_heading, resolve_title
from ._base import DocMixin
from ._utils import check_align


class HeadingMixin(DocMixin):
    """Adds title() and h1()..h6() to Report."""

    def _add_heading(
        self,
        level: int,
        text: str,
        align: Optional[AlignLiteral],
    ) -> 'HeadingMixin':
        check_align(align, where=f'heading level {level}')
        local: dict[str, Any] = {'align': align}
        if level == 0:
            resolved = resolve_title(self.config, local)
        else:
            resolved = resolve_heading(self.config, level, local)
        para = self.doc.add_heading(text, level=level)
        alignment = ALIGN[resolved.align]
        if alignment is not None:
            para.alignment = alignment
        return self

    def title(self, text: str,
              align: Optional[AlignLiteral] = None) -> 'HeadingMixin':
        """Add a title (level 0 heading)."""
        return self._add_heading(0, text, align)

    def h1(self, text: str,
           align: Optional[AlignLiteral] = None) -> 'HeadingMixin':
        """Add a level-1 heading."""
        return self._add_heading(1, text, align)

    def h2(self, text: str,
           align: Optional[AlignLiteral] = None) -> 'HeadingMixin':
        """Add a level-2 heading."""
        return self._add_heading(2, text, align)

    def h3(self, text: str,
           align: Optional[AlignLiteral] = None) -> 'HeadingMixin':
        """Add a level-3 heading."""
        return self._add_heading(3, text, align)

    def h4(self, text: str,
           align: Optional[AlignLiteral] = None) -> 'HeadingMixin':
        """Add a level-4 heading."""
        return self._add_heading(4, text, align)

    def h5(self, text: str,
           align: Optional[AlignLiteral] = None) -> 'HeadingMixin':
        """Add a level-5 heading."""
        return self._add_heading(5, text, align)

    def h6(self, text: str,
           align: Optional[AlignLiteral] = None) -> 'HeadingMixin':
        """Add a level-6 heading."""
        return self._add_heading(6, text, align)