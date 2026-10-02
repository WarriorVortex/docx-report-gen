"""List mixin."""
from ..styles import ALIGN, LIST_BULLET_STYLES, LIST_NUMBER_STYLES, resolve_list
from ._base import DocMixin


class ListMixin(DocMixin):
    """Adds ul() and ol() to Report.

    Items can be strings, or nested lists/tuples for sub-levels.
    Nesting is limited to three levels (Word's built-in styles).
    """

    def ul(self, items, align=None):
        """Bulleted list."""
        return self._render_list(items, LIST_BULLET_STYLES, 1, align)

    def ol(self, items, align=None):
        """Numbered list."""
        return self._render_list(items, LIST_NUMBER_STYLES, 1, align)

    def _render_list(self, items, style_names, level, align):
        if level > len(style_names):
            return self
        resolved = resolve_list(self.config, {'align': align})
        style_name = style_names[level - 1]
        for item in items:
            if isinstance(item, (list, tuple)):
                self._render_list(item, style_names, level + 1, align)
            else:
                para = self.doc.add_paragraph(style=style_name)
                para.alignment = ALIGN[resolved.align]
                para.add_run(str(item))
        return self