"""Full document style configuration."""
from dataclasses import dataclass, field
from typing import Optional

from .caption import CaptionStyle
from .code import CodeStyle
from .heading import HeadingStyle
from .image import ImageStyle
from .list import ListStyle
from .paragraph import ParagraphStyle
from .quote import QuoteStyle
from .table import TableStyle
from .types import RGB


@dataclass
class StylesConfig:
    """Full document style configuration.

    Per-element resolution order (see styles.utils.resolve):
      1. local argument passed to a method
      2. element subconfig
      3. global fields of this config (font / size / color / align)
      4. dataclass defaults of the subconfig itself
    """

    font: str = 'Times New Roman'
    size: int = 12
    color: RGB = (0, 0, 0)
    align: str = 'left'

    margins: Optional[tuple[float, float, float, float]] = None

    # Headings.
    heading: HeadingStyle = field(default_factory=lambda: HeadingStyle(
        bold=True, color=(0, 0, 0), align='left',
    ))
    heading_sizes: tuple[int, ...] = (16, 14, 13, 12, 12, 12)
    heading_overrides: dict[int, HeadingStyle] = field(default_factory=dict)
    title: HeadingStyle = field(default_factory=lambda: HeadingStyle(
        size=20, align='center', color=(0, 0, 0),
    ))

    # Body content.
    paragraph: ParagraphStyle = field(default_factory=ParagraphStyle)
    formula: ParagraphStyle = field(
        default_factory=lambda: ParagraphStyle(align='center'),
    )

    # Lists, code, quotes.
    list: ListStyle = field(default_factory=ListStyle)
    code: CodeStyle = field(default_factory=CodeStyle)
    quote: QuoteStyle = field(default_factory=QuoteStyle)

    # Tables.
    table: TableStyle = field(default_factory=TableStyle)

    # Captions.
    caption: CaptionStyle = field(default_factory=CaptionStyle)
    image_caption: CaptionStyle = field(default_factory=lambda: CaptionStyle(
        prefix='Рисунок',
        template='{prefix} {n} — {caption}',
        align='center',
    ))

    # Images.
    image: ImageStyle = field(default_factory=ImageStyle)