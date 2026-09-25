"""Report method mixins."""
from ._base import DocMixin
from .headings import HeadingMixin
from .paragraphs import ParagraphMixin
from .tables import TableMixin

__all__ = ['DocMixin', 'HeadingMixin', 'ParagraphMixin', 'TableMixin']