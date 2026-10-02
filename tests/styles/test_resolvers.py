"""Tests for styles.resolvers — domain-specific resolution helpers."""
from docx_report_gen.styles import (
    HeadingStyle, ParagraphStyle, StylesConfig,
)
from docx_report_gen.styles.resolvers import (
    resolve_caption, resolve_code, resolve_formula, resolve_heading,
    resolve_image, resolve_image_caption, resolve_list,
    resolve_paragraph, resolve_quote, resolve_table, resolve_title,
)


# ---------- simple resolvers ----------

def test_resolve_title_uses_config_title():
    config = StylesConfig()
    result = resolve_title(config)
    assert result.align == 'center'
    assert result.size == 20


def test_resolve_title_local_overrides():
    config = StylesConfig()
    result = resolve_title(config, {'align': 'left'})
    assert result.align == 'left'


def test_resolve_paragraph_defaults_from_config():
    config = StylesConfig()
    result = resolve_paragraph(config)
    # StylesConfig.paragraph has no explicit align, so global align applies.
    assert result.align == 'left'


def test_resolve_paragraph_local_align():
    config = StylesConfig()
    result = resolve_paragraph(config, {'align': 'justify'})
    assert result.align == 'justify'


def test_resolve_formula_defaults_to_center():
    config = StylesConfig()
    result = resolve_formula(config)
    assert result.align == 'center'


def test_resolve_caption_defaults_from_config():
    config = StylesConfig()
    result = resolve_caption(config)
    assert result.prefix == 'Таблица'


def test_resolve_image_caption_defaults():
    config = StylesConfig()
    result = resolve_image_caption(config)
    assert result.prefix == 'Рисунок'
    assert result.align == 'center'


def test_resolve_image_falls_back_to_global_align():
    """ImageStyle has `align`; StylesConfig has `align='left'` by default.
    The global value flows through the resolver."""
    config = StylesConfig()
    result = resolve_image(config)
    assert result.align == 'left'


def test_resolve_image_local_align_wins():
    config = StylesConfig()
    result = resolve_image(config, {'align': 'center'})
    assert result.align == 'center'


def test_resolve_image_width_from_config():
    from docx_report_gen.styles import ImageStyle
    config = StylesConfig(image=ImageStyle(width=10))
    result = resolve_image(config)
    assert result.width == 10


def test_resolve_list_uses_config():
    config = StylesConfig()
    result = resolve_list(config, {'align': 'left'})
    assert result.align == 'left'


def test_resolve_code_uses_config():
    config = StylesConfig()
    result = resolve_code(config)
    assert result.font == 'Consolas'


def test_resolve_quote_uses_config():
    config = StylesConfig()
    result = resolve_quote(config)
    assert result.italic is True


def test_resolve_table_uses_config():
    config = StylesConfig()
    result = resolve_table(config, {'align': 'center'})
    assert result.align == 'center'


# ---------- heading_sizes ----------

def test_resolve_heading_picks_size_from_heading_sizes():
    config = StylesConfig(heading_sizes=(20, 18, 16, 14, 12, 10))
    for level, expected_size in enumerate((20, 18, 16, 14, 12, 10), start=1):
        result = resolve_heading(config, level)
        assert result.size == expected_size, (
            f'H{level} expected size {expected_size}, got {result.size}'
        )


def test_resolve_heading_level_out_of_range_keeps_base_size():
    """A level beyond len(heading_sizes) falls back to heading.size."""
    config = StylesConfig(heading=HeadingStyle(size=99))
    result = resolve_heading(config, 10)
    assert result.size == 99


def test_resolve_heading_local_align_wins():
    config = StylesConfig()
    result = resolve_heading(config, 1, {'align': 'center'})
    assert result.align == 'center'


# ---------- heading_overrides ----------

def test_resolve_heading_per_level_override():
    config = StylesConfig(
        heading=HeadingStyle(align='left'),
        heading_overrides={2: HeadingStyle(align='center')},
    )
    h1 = resolve_heading(config, 1)
    h2 = resolve_heading(config, 2)
    assert h1.align == 'left'
    assert h2.align == 'center'


def test_resolve_heading_per_level_size_override():
    """heading_overrides wins over heading_sizes for the same field."""
    config = StylesConfig(
        heading_sizes=(20, 18, 16, 14, 12, 10),
        heading_overrides={2: HeadingStyle(size=15)},
    )
    h2 = resolve_heading(config, 2)
    assert h2.size == 15


def test_resolve_heading_per_level_partial_override():
    """An override that sets only align keeps size from heading_sizes."""
    config = StylesConfig(
        heading_sizes=(20, 18, 16, 14, 12, 10),
        heading_overrides={2: HeadingStyle(align='right')},
    )
    h2 = resolve_heading(config, 2)
    assert h2.align == 'right'
    assert h2.size == 18


# ---------- global fallbacks ----------

def test_resolve_heading_inherits_global_font():
    config = StylesConfig(font='Georgia')
    result = resolve_heading(config, 1)
    assert result.font == 'Georgia'


def test_resolve_paragraph_inherits_global_align():
    config = StylesConfig(align='right')
    result = resolve_paragraph(config)
    assert result.align == 'right'


def test_resolve_local_align_from_mixin_style_dict():
    """Mimics the {'align': ...} dict that mixins pass."""
    config = StylesConfig()
    result = resolve_heading(config, 1, {'align': 'left'})
    assert result.align == 'left'