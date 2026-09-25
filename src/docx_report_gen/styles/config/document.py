"""Full document style configuration."""
from dataclasses import dataclass, field
from typing import Optional

from .caption import CaptionStyle
from .heading import HeadingStyle
from .types import RGB


@dataclass
class StylesConfig:
    """Full document style configuration."""

    # Base ("Normal") paragraph style.
    font: str = 'Times New Roman'
    size: int = 12
    color: RGB = (0, 0, 0)

    # Page margins in cm: (top, right, bottom, left). None = keep defaults.
    margins: Optional[tuple[float, float, float, float]] = None

    # Applied to every H1..H6 unless overridden by `heading_overrides`.
    heading: HeadingStyle = field(default_factory=lambda: HeadingStyle(
        bold=True, color=(0, 0, 0), align='left',
    ))

    # Sizes for H1..H6. A shorter tuple configures only the first N levels.
    heading_sizes: tuple[int, ...] = (18, 16, 14, 13, 12, 12)

    # Per-level overrides, e.g. {2: HeadingStyle(align='center')}.
    heading_overrides: dict[int, HeadingStyle] = field(default_factory=dict)

    # Title (level 0) — separate from headings.
    title: HeadingStyle = field(default_factory=lambda: HeadingStyle(
        size=20, align='center', color=(0, 0, 0),
    ))

    # Table captions. Default: left-aligned, "Таблица N — ...".
    caption: CaptionStyle = field(default_factory=CaptionStyle)

    # Image captions. Default: centered, "Рисунок N — ...".
    image_caption: CaptionStyle = field(default_factory=lambda: CaptionStyle(
        prefix='Рисунок',
        template='{prefix} {n} — {caption}',
        align='center',
    ))