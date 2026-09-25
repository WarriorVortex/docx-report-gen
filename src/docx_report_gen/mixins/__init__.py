"""Report method mixins."""
from ._base import DocMixin
from .headings import HeadingMixin
from .images import ImageMixin
from .layout import LayoutMixin
from .paragraphs import ParagraphMixin
from .tables import TableMixin

__all__ = [
    'DocMixin',
    'HeadingMixin',
    'ImageMixin',
    'LayoutMixin',
    'ParagraphMixin',
    'TableMixin',
]