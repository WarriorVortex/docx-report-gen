"""Domain-specific style resolution helpers."""
from typing import Any, Optional

from .config import (
    CaptionStyle, CodeStyle, HeadingStyle, ImageStyle,
    ListStyle, ParagraphStyle, QuoteStyle, TableStyle, StylesConfig,
)
from .utils import resolve


LocalOverride = Optional[dict[str, Any]]
"""A partial style passed from a mixin: {'align': 'right'} etc.

Only fields present in the dict take precedence; missing fields fall
through to the subconfig and then to the global StylesConfig.
"""


def resolve_title(
    config: StylesConfig,
    local: LocalOverride = None,
) -> HeadingStyle:
    """Resolve HeadingStyle for the title (level 0)."""
    return resolve(HeadingStyle, local, config.title, config)


def resolve_heading(
    config: StylesConfig,
    level: int,
    local: LocalOverride = None,
) -> HeadingStyle:
    """Resolve HeadingStyle for level 1..6.

    Sources: local override → heading_overrides[level] → heading
    (with size taken from heading_sizes) → global config.
    """
    from dataclasses import replace
    sub = config.heading
    if 0 < level <= len(config.heading_sizes):
        sub = replace(sub, size=config.heading_sizes[level - 1])
    return resolve(
        HeadingStyle,
        local,
        config.heading_overrides.get(level),
        sub,
        config,
    )


def resolve_paragraph(
    config: StylesConfig,
    local: LocalOverride = None,
) -> ParagraphStyle:
    """Resolve ParagraphStyle for body text."""
    return resolve(ParagraphStyle, local, config.paragraph, config)


def resolve_formula(
    config: StylesConfig,
    local: LocalOverride = None,
) -> ParagraphStyle:
    """Resolve ParagraphStyle for standalone formulas."""
    return resolve(ParagraphStyle, local, config.formula, config)


def resolve_caption(
    config: StylesConfig,
    local: LocalOverride = None,
) -> CaptionStyle:
    """Resolve CaptionStyle for table captions."""
    return resolve(CaptionStyle, local, config.caption, config)


def resolve_image_caption(
    config: StylesConfig,
    local: LocalOverride = None,
) -> CaptionStyle:
    """Resolve CaptionStyle for image captions."""
    return resolve(CaptionStyle, local, config.image_caption, config)


def resolve_image(
    config: StylesConfig,
    local: LocalOverride = None,
) -> ImageStyle:
    """Resolve ImageStyle for the image itself."""
    return resolve(ImageStyle, local, config.image, config)


def resolve_list(
    config: StylesConfig,
    local: LocalOverride = None,
) -> ListStyle:
    """Resolve ListStyle for bullet and numbered lists."""
    return resolve(ListStyle, local, config.list, config)


def resolve_code(
    config: StylesConfig,
    local: LocalOverride = None,
) -> CodeStyle:
    """Resolve CodeStyle for code blocks."""
    return resolve(CodeStyle, local, config.code, config)


def resolve_quote(
    config: StylesConfig,
    local: LocalOverride = None,
) -> QuoteStyle:
    """Resolve QuoteStyle for block quotes."""
    return resolve(QuoteStyle, local, config.quote, config)


def resolve_table(
    config: StylesConfig,
    local: LocalOverride = None,
) -> TableStyle:
    """Resolve TableStyle for tables."""
    return resolve(TableStyle, local, config.table, config)