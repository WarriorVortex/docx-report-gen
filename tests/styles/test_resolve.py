"""Tests for styles.utils.resolve — the three-level priority chain."""
import pytest

from docx_report_gen.styles import (
    CaptionStyle, HeadingStyle, ParagraphStyle, StylesConfig,
)
from docx_report_gen.styles.utils import resolve


# ---------- priority chain ----------

def test_resolve_returns_instance_of_target_class():
    result = resolve(HeadingStyle)
    assert isinstance(result, HeadingStyle)


def test_resolve_uses_dataclass_default_when_no_source():
    """No sources at all -> every field keeps its declared default."""
    result = resolve(HeadingStyle)
    assert result.font is None
    assert result.align is None
    assert result.bold is None


def test_resolve_picks_value_from_single_source():
    source = HeadingStyle(font='Arial', size=14)
    result = resolve(HeadingStyle, source)
    assert result.font == 'Arial'
    assert result.size == 14


def test_local_overrides_subconfig():
    sub = HeadingStyle(font='Arial', size=14, bold=True)
    local = HeadingStyle(font='Times New Roman')
    result = resolve(HeadingStyle, local, sub)
    assert result.font == 'Times New Roman'   # local wins
    assert result.size == 14                   # sub fills the rest
    assert result.bold is True


def test_subconfig_overrides_global():
    sub = HeadingStyle(align='center')
    global_config = StylesConfig(align='left')
    result = resolve(HeadingStyle, sub, global_config)
    assert result.align == 'center'


def test_global_used_when_nothing_else_defines_field():
    global_config = StylesConfig(font='Georgia', size=11, align='justify')
    result = resolve(HeadingStyle, None, None, global_config)
    assert result.font == 'Georgia'
    assert result.size == 11
    assert result.align == 'justify'


def test_none_sources_are_skipped():
    mid = HeadingStyle(size=15)
    result = resolve(HeadingStyle, None, mid, None)
    assert result.size == 15


def test_full_chain_prefers_first_non_none():
    local = HeadingStyle(font='Local')
    sub = HeadingStyle(font='Sub', size=20)
    global_config = StylesConfig(font='Global', size=10, align='left')
    result = resolve(HeadingStyle, local, sub, global_config)
    assert result.font == 'Local'   # from local
    assert result.size == 20        # from sub
    assert result.align == 'left'   # from global


# ---------- dict sources ----------

def test_dict_source_is_accepted():
    result = resolve(HeadingStyle, {'font': 'Arial', 'size': 13})
    assert result.font == 'Arial'
    assert result.size == 13


def test_dict_with_none_values_is_skipped():
    """A dict entry with value None does not override the next source."""
    sub = HeadingStyle(font='Arial')
    result = resolve(HeadingStyle, {'font': None}, sub)
    assert result.font == 'Arial'


def test_dict_partial_does_not_clobber_other_fields():
    sub = HeadingStyle(font='Arial', size=14, bold=True)
    local = {'align': 'center'}
    result = resolve(HeadingStyle, local, sub)
    assert result.align == 'center'
    assert result.font == 'Arial'
    assert result.size == 14
    assert result.bold is True


# ---------- attribute-missing sources ----------

def test_source_without_matching_attribute_is_skipped():
    """A StylesConfig has no `bold` field; that must not raise."""
    config = StylesConfig(font='Arial')
    result = resolve(HeadingStyle, config)
    assert result.font == 'Arial'
    assert result.bold is None


# ---------- align validation ----------

@pytest.mark.parametrize('bad', ['centre', 'top', 'justified', ''])
def test_invalid_align_raises_value_error(bad):
    with pytest.raises(ValueError, match='align'):
        resolve(HeadingStyle, {'align': bad})


@pytest.mark.parametrize('good', ['left', 'center', 'right', 'justify'])
def test_valid_align_accepted(good):
    result = resolve(HeadingStyle, {'align': good})
    assert result.align == good


def test_none_align_is_allowed():
    result = resolve(HeadingStyle, {'align': None})
    assert result.align is None


# ---------- genericity ----------

def test_resolve_works_for_caption_style():
    sub = CaptionStyle(prefix='Table', align='left')
    result = resolve(CaptionStyle, sub)
    assert result.prefix == 'Table'
    assert result.align == 'left'
    assert result.template == '{prefix} {n} — {caption}'   # default


def test_resolve_works_for_paragraph_style():
    sub = ParagraphStyle(align='justify', line_spacing=1.5)
    result = resolve(ParagraphStyle, sub)
    assert result.align == 'justify'
    assert result.line_spacing == 1.5
    assert result.left_indent is None


def test_global_align_fills_paragraph_style_align():
    """ParagraphStyle has `align`, StylesConfig has `align`.
    The three-level chain pulls the global value into the target."""
    config = StylesConfig(align='right')
    result = resolve(ParagraphStyle, config)
    assert result.align == 'right'


def test_layout_fields_absent_from_global_stay_unset():
    """StylesConfig has no `line_spacing`; the target keeps its default."""
    config = StylesConfig(align='right', font='Arial')
    result = resolve(ParagraphStyle, config)
    assert result.line_spacing is None
    assert result.space_before is None
    assert result.first_line_indent is None
    assert result.left_indent is None