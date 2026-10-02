"""Tests for ParagraphMixin — p, f, quote, layout, formula numbering."""
import pytest

from docx_report_gen import Report, StylesConfig, QuoteStyle
from docx_report_gen.docx import to_twips
from docx_report_gen.inline import b, i

from ._helpers import (
    document_xml, paragraphs_xml, paragraph_alignment, paragraph_indent,
    paragraph_spacing, paragraph_style_id, paragraph_tab_stops,
    paragraph_text,
)


# ---------- p() basics ----------

def test_p_creates_paragraph_with_text(report, docx_path):
    report.p('Hello world')
    report.save(str(docx_path))
    paras = paragraphs_xml(docx_path)
    assert paragraph_text(paras[0]) == 'Hello world'


def test_p_with_multiple_string_parts(report, docx_path):
    report.p('a', 'b', 'c')
    report.save(str(docx_path))
    paras = paragraphs_xml(docx_path)
    assert paragraph_text(paras[0]) == 'abc'


def test_p_with_inline_nodes(report, docx_path):
    report.p('a', b('B'), i('I'))
    report.save(str(docx_path))
    paras = paragraphs_xml(docx_path)
    assert paragraph_text(paras[0]) == 'aBI'


def test_p_rejects_non_string_non_inline(report):
    with pytest.raises(TypeError, match='inline nodes'):
        report.p('text', 123)


def test_p_empty_is_valid(report, docx_path):
    report.p()
    report.save(str(docx_path))
    paras = paragraphs_xml(docx_path)
    assert paragraph_text(paras[0]) == ''


def test_p_returns_self_for_chaining(report):
    assert report.p('x') is report


# ---------- p() alignment resolution ----------

def test_p_default_align_from_global(docx_path):
    config = StylesConfig(align='justify')
    r = Report(config=config)
    r.p('X')
    r.save(str(docx_path))
    paras = paragraphs_xml(docx_path)
    assert paragraph_alignment(paras[0]) == 'both'


def test_p_local_align_overrides(docx_path):
    r = Report()
    r.p('X', align='center')
    r.save(str(docx_path))
    paras = paragraphs_xml(docx_path)
    assert paragraph_alignment(paras[0]) == 'center'


def test_p_invalid_align_raises(report):
    with pytest.raises(ValueError):
        report.p('X', align='centre')


# ---------- p() layout ----------

def test_p_line_spacing(docx_path):
    r = Report()
    r.p('X', line_spacing=1.5)
    r.save(str(docx_path))
    paras = paragraphs_xml(docx_path)
    spacing = paragraph_spacing(paras[0])
    # 1.5 line spacing -> 360 twips (240 * 1.5)
    assert spacing.get('line') == 360


def test_p_space_before_after(docx_path):
    r = Report()
    r.p('X', space_before=6, space_after=12)
    r.save(str(docx_path))
    paras = paragraphs_xml(docx_path)
    spacing = paragraph_spacing(paras[0])
    # points to twentieths of a point
    assert spacing.get('before') == to_twips(6, 'pt')
    assert spacing.get('after') == to_twips(12, 'pt')


def test_p_first_line_indent(docx_path):
    r = Report()
    r.p('X', first_line_indent=1.25)
    r.save(str(docx_path))
    paras = paragraphs_xml(docx_path)
    indent = paragraph_indent(paras[0])
    assert indent.get('firstLine') == to_twips(1.25, 'cm')


# ---------- block formula f() ----------

def test_f_without_number_centers(report, docx_path):
    report.f('E = mc^2')
    report.save(str(docx_path))
    paras = paragraphs_xml(docx_path)
    assert paragraph_alignment(paras[0]) == 'center'


def test_f_local_align(docx_path):
    r = Report()
    r.f('x', align='left')
    r.save(str(docx_path))
    paras = paragraphs_xml(docx_path)
    assert paragraph_alignment(paras[0]) == 'left'


def test_f_omath_present(report, docx_path):
    report.f('x^2')
    report.save(str(docx_path))
    xml = document_xml(docx_path)
    M = 'http://schemas.openxmlformats.org/officeDocument/2006/math'
    assert len(xml.findall(f'.//{{{M}}}oMath')) == 1


# ---------- numbered formulas ----------

def test_f_numbered_has_tab_stops(report, docx_path):
    report.f('x^2', number=True)
    report.save(str(docx_path))
    paras = paragraphs_xml(docx_path)
    stops = paragraph_tab_stops(paras[0])
    assert len(stops) == 2
    alignments = [s[1] for s in stops]
    assert 'center' in alignments
    assert 'right' in alignments


def test_f_numbered_adds_paren_number(report, docx_path):
    report.f('x^2', number=True)
    report.save(str(docx_path))
    paras = paragraphs_xml(docx_path)
    text = paragraph_text(paras[0])
    assert '(1)' in text


def test_f_counter_increments_per_report(report, docx_path):
    report.f('a', number=True)
    report.f('b', number=True)
    report.f('c', number=True)
    report.save(str(docx_path))
    paras = paragraphs_xml(docx_path)
    texts = [paragraph_text(p) for p in paras]
    assert '(1)' in texts[0]
    assert '(2)' in texts[1]
    assert '(3)' in texts[2]


def test_f_counter_independent_between_reports(docx_path):
    r1 = Report()
    r1.f('a', number=True)
    r1.save(str(docx_path))

    r2 = Report()
    r2.f('b', number=True)
    path2 = docx_path.parent / 'second.docx'
    r2.save(str(path2))

    paras1 = paragraphs_xml(docx_path)
    paras2 = paragraphs_xml(path2)
    assert '(1)' in paragraph_text(paras1[0])
    assert '(1)' in paragraph_text(paras2[0])


def test_f_numbered_not_numbered_mix(report, docx_path):
    """Unnumbered formulas do not consume the counter."""
    report.f('a', number=True)
    report.f('b')                  # no counter
    report.f('c', number=True)
    report.save(str(docx_path))

    paras = paragraphs_xml(docx_path)
    texts = [paragraph_text(p) for p in paras]
    assert '(1)' in texts[0]
    assert texts[1] == ''          # unnumbered, no text
    assert '(2)' in texts[2]


# ---------- quote() ----------

def test_quote_creates_paragraph_with_style(report, docx_path):
    report.quote('A quoted line.')
    report.save(str(docx_path))
    paras = paragraphs_xml(docx_path)
    assert paragraph_text(paras[0]) == 'A quoted line.'
    assert paragraph_style_id(paras[0]) == 'ReportQuote'


def test_quote_with_inline_nodes(report, docx_path):
    report.quote('See ', b('this'), '.')
    report.save(str(docx_path))
    paras = paragraphs_xml(docx_path)
    assert paragraph_text(paras[0]) == 'See this.'


def test_quote_rejects_bad_part(report):
    with pytest.raises(TypeError):
        report.quote('text', 42)


def test_quote_left_indent_local(docx_path):
    r = Report()
    r.quote('X', left_indent=2.0)
    r.save(str(docx_path))
    paras = paragraphs_xml(docx_path)
    indent = paragraph_indent(paras[0])
    assert indent.get('left') == to_twips(2.0, 'cm')


def test_quote_uses_config_defaults(docx_path):
    config = StylesConfig(
        quote=QuoteStyle(italic=True, left_indent=1.0, align='justify'),
    )
    r = Report(config=config)
    r.quote('X')
    r.save(str(docx_path))
    paras = paragraphs_xml(docx_path)
    assert paragraph_alignment(paras[0]) == 'both'
    indent = paragraph_indent(paras[0])
    assert indent.get('left') == to_twips(1.0, 'cm')