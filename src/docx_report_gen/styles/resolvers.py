"""Domain-specific style resolution helpers.

Each resolver builds the source chain for a specific element and
delegates to `resolve`. Both mixins and `styles.apply` use these, so
that the same priorities apply everywhere.
"""
from dataclasses import replace

from .config import (
    CaptionStyle, HeadingStyle, ImageStyle, ParagraphStyle,
)
from .utils import resolve


def resolve_title(config, local=None):
    """Resolve HeadingStyle for the title (level 0)."""
    return resolve(HeadingStyle, local, config.title, config)


def resolve_heading(config, level, local=None):
    """Resolve HeadingStyle for level 1..6.

    Sources: local override → heading_overrides[level] → heading
    (with size taken from heading_sizes) → global config.
    """
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


def resolve_paragraph(config, local=None):
    """Resolve ParagraphStyle for body text."""
    return resolve(ParagraphStyle, local, config.paragraph, config)


def resolve_formula(config, local=None):
    """Resolve ParagraphStyle for standalone formulas."""
    return resolve(ParagraphStyle, local, config.formula, config)


def resolve_caption(config, local=None):
    """Resolve CaptionStyle for table captions."""
    return resolve(CaptionStyle, local, config.caption, config)


def resolve_image_caption(config, local=None):
    """Resolve CaptionStyle for image captions."""
    return resolve(CaptionStyle, local, config.image_caption, config)


def resolve_image(config, local=None):
    """Resolve ImageStyle for the image itself."""
    return resolve(ImageStyle, local, config.image, config)