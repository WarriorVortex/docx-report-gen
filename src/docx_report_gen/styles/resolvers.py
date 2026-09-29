"""Domain-specific style resolution helpers."""
from dataclasses import replace

from .config import (
    CaptionStyle, CodeStyle, HeadingStyle, ImageStyle,
    ListStyle, ParagraphStyle, QuoteStyle,
)
from .utils import resolve


def resolve_title(config, local=None):
    return resolve(HeadingStyle, local, config.title, config)


def resolve_heading(config, level, local=None):
    sub = config.heading
    if 0 < level <= len(config.heading_sizes):
        sub = replace(sub, size=config.heading_sizes[level - 1])
    return resolve(
        HeadingStyle,
        local, config.heading_overrides.get(level), sub, config,
    )


def resolve_paragraph(config, local=None):
    return resolve(ParagraphStyle, local, config.paragraph, config)


def resolve_formula(config, local=None):
    return resolve(ParagraphStyle, local, config.formula, config)


def resolve_caption(config, local=None):
    return resolve(CaptionStyle, local, config.caption, config)


def resolve_image_caption(config, local=None):
    return resolve(CaptionStyle, local, config.image_caption, config)


def resolve_image(config, local=None):
    return resolve(ImageStyle, local, config.image, config)


def resolve_list(config, local=None):
    return resolve(ListStyle, local, config.list, config)


def resolve_code(config, local=None):
    return resolve(CodeStyle, local, config.code, config)


def resolve_quote(config, local=None):
    return resolve(QuoteStyle, local, config.quote, config)