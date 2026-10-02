"""List mixin."""
from typing import Optional, Sequence, Union

from ..styles import (
    ALIGN, LIST_BULLET_STYLES, LIST_NUMBER_STYLES, AlignLiteral,
    resolve_list,
)
from ._base import DocMixin
from ._utils import check_align


ListItem = Union[str, Sequence['ListItem']]
"""A list item: either a string, or a nested sequence for the next level."""


class ListMixin(DocMixin):
    """Adds ul() and ol() to Report.

    Items can be strings, or nested lists/tuples for sub-levels.
    Nesting is limited to three levels (Word's built-in styles).
    """

    def ul(
        self,
        items: Sequence[ListItem],
        align: Optional[AlignLiteral] = None,
    ) -> 'ListMixin':
        """Bulleted list."""
        return self._render_list(
            items, LIST_BULLET_STYLES, 1, align, 'ul',
        )

    def ol(
        self,
        items: Sequence[ListItem],
        align: Optional[AlignLiteral] = None,
    ) -> 'ListMixin':
        """Numbered list."""
        return self._render_list(
            items, LIST_NUMBER_STYLES, 1, align, 'ol',
        )

    def _render_list(
        self,
        items: Sequence[ListItem],
        style_names: tuple[str, ...],
        level: int,
        align: Optional[AlignLiteral],
        where: str,
    ) -> 'ListMixin':
        check_align(align, where=where)
        if level > len(style_names):
            return self
        resolved = resolve_list(self.config, {'align': align})
        style_name = style_names[level - 1]
        for item in items:
            if isinstance(item, (list, tuple)):
                self._render_list(item, style_names, level + 1, align, where)
            else:
                para = self.doc.add_paragraph(style=style_name)
                alignment = ALIGN[resolved.align]
                if alignment is not None:
                    para.alignment = alignment
                para.add_run(str(item))
        return self