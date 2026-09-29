"""Report method mixins."""
from ._base import DocMixin
from .code import CodeMixin
from .headings import HeadingMixin
from .images import ImageMixin
from .layout import LayoutMixin
from .lists import ListMixin
from .paragraphs import ParagraphMixin
from .tables import TableMixin

__all__ = [
    'DocMixin',
    'CodeMixin',
    'HeadingMixin',
    'ImageMixin',
    'LayoutMixin',
    'ListMixin',
    'ParagraphMixin',
    'TableMixin',
]