"""Tests for style configuration dataclasses and their defaults."""
from docx_report_gen.styles import (
    CaptionStyle, CodeStyle, HeadingStyle, ImageStyle,
    LayoutStyle, ListStyle, ParagraphStyle, QuoteStyle,
    StylesConfig, TableStyle,
)


# ---------- StylesConfig defaults ----------

def test_styles_config_defaults():
    config = StylesConfig()
    assert config.font == 'Times New Roman'
    assert config.size == 12
    assert config.color == (0, 0, 0)
    assert config.align == 'left'
    assert config.margins is None


def test_styles_config_default_heading():
    config = StylesConfig()
    assert isinstance(config.heading, HeadingStyle)
    assert config.heading.bold is True
    assert config.heading.align == 'left'


def test_styles_config_default_title():
    config = StylesConfig()
    assert config.title.align == 'center'
    assert config.title.size == 20


def test_styles_config_default_caption_and_image_caption():
    config = StylesConfig()
    assert config.caption.prefix == 'Таблица'
    assert config.image_caption.prefix == 'Рисунок'
    assert config.image_caption.align == 'center'


def test_styles_config_heading_sizes_length():
    config = StylesConfig()
    assert len(config.heading_sizes) == 6


def test_styles_config_explicit_values():
    config = StylesConfig(
        font='Arial',
        size=11,
        color=(10, 20, 30),
        align='justify',
        margins=(2.0, 1.0, 2.0, 3.0),
    )
    assert config.font == 'Arial'
    assert config.size == 11
    assert config.color == (10, 20, 30)
    assert config.align == 'justify'
    assert config.margins == (2.0, 1.0, 2.0, 3.0)


def test_styles_config_heading_overrides_is_per_instance():
    """Two configs must not share the same heading_overrides dict."""
    a = StylesConfig()
    b = StylesConfig()
    a.heading_overrides[1] = HeadingStyle(align='center')
    assert b.heading_overrides == {}


def test_styles_config_subconfigs_are_per_instance():
    a = StylesConfig()
    b = StylesConfig()
    assert a.heading is not b.heading
    assert a.caption is not b.caption
    assert a.image_caption is not b.image_caption


# ---------- LayoutStyle inheritance ----------

def test_layout_style_fields_present():
    layout = LayoutStyle()
    assert layout.align is None
    assert layout.line_spacing is None
    assert layout.space_before is None
    assert layout.space_after is None
    assert layout.first_line_indent is None
    assert layout.left_indent is None


def test_paragraph_style_inherits_layout_fields():
    ps = ParagraphStyle(align='justify', line_spacing=1.5, space_after=6)
    assert ps.align == 'justify'
    assert ps.line_spacing == 1.5
    assert ps.space_after == 6


def test_code_style_has_font_and_background():
    cs = CodeStyle()
    assert cs.font == 'Consolas'
    assert cs.size == 10
    assert cs.background == 'F5F5F5'


def test_code_style_inherits_layout_fields():
    cs = CodeStyle(align='left', line_spacing=1.0)
    assert cs.align == 'left'
    assert cs.line_spacing == 1.0


def test_code_style_background_empty_string_is_allowed():
    """`background=''` means no shading; None means 'inherit'."""
    cs = CodeStyle(background='')
    assert cs.background == ''


def test_quote_style_defaults():
    qs = QuoteStyle()
    assert qs.italic is True
    assert qs.left_indent is None


def test_quote_style_inherits_layout_fields():
    qs = QuoteStyle(align='justify', left_indent=1.5, line_spacing=1.15)
    assert qs.align == 'justify'
    assert qs.left_indent == 1.5
    assert qs.line_spacing == 1.15


def test_list_style_defaults():
    ls = ListStyle()
    assert ls.align is None
    assert ls.left_indent is None
    assert ls.font is None
    assert ls.size is None
    assert ls.color is None


def test_list_style_inherits_layout_fields():
    """ListStyle is a LayoutStyle subclass like the other content styles."""
    ls = ListStyle(align='left', left_indent=0.75, line_spacing=1.0)
    assert ls.align == 'left'
    assert ls.left_indent == 0.75
    assert ls.line_spacing == 1.0


def test_table_style_defaults():
    ts = TableStyle()
    assert ts.align is None
    assert ts.col_widths is None
    assert ts.col_aligns is None
    assert ts.header_align is None


def test_image_style_defaults():
    ist = ImageStyle()
    assert ist.align is None
    assert ist.width is None


def test_caption_style_defaults():
    cs = CaptionStyle()
    assert cs.prefix == 'Таблица'
    assert cs.template == '{prefix} {n} — {caption}'
    assert cs.align is None


def test_heading_style_defaults():
    hs = HeadingStyle()
    assert hs.font is None
    assert hs.size is None
    assert hs.bold is None
    assert hs.italic is None
    assert hs.color is None
    assert hs.align is None