"""Layout methods mixin."""
from ._base import DocMixin


class LayoutMixin(DocMixin):
    """Adds page_break() and other layout primitives to Report."""

    def page_break(self):
        """Insert a page break."""
        self.doc.add_page_break()
        return self