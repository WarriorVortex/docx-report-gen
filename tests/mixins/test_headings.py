"""Tests for HeadingMixin — title, h1..h6, alignment resolution."""
import pytest

from docx_report_gen import Report, StylesConfig, HeadingStyle

from ._helpers import paragraphs_xml, paragraph_alignment, paragraph_text


# ---------- levels ----------

def test_title_creates_title_paragraph(report, docx_path):
    report.title('Hello')
    report.save(str(docx_path))
    paras = paragraphs_xml(docx_path)
    assert paragraph_text(paras[0]) == 'Hello'


def test_h1_through_h6_create_expected_paragraphs(report, docx_path):
    for level in range(1, 7):
        getattr(report, f'h{level}')(f'Level {level}')
    report.save(str(docx_path))

    paras = paragraphs_xml(docx_path)
    texts = [paragraph_text(p) for p in paras]
    for level in range(1, 7):
        assert f'Level {level}' in texts


def test_h1_style_is_heading1(report, docx_path):
    report.h1('X')
    report.save(str(docx_path))
    paras = paragraphs_xml(docx_path)
    W = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
    p_pr = paras[0].find(f'{{{W}}}pPr')
    style = p_pr.find(f'{{{W}}}pStyle')
    assert style is not None
    assert style.get(f'{{{W}}}val') == 'Heading1'


# ---------- alignment resolution ----------

def test_default_heading_align_is_left(docx_path):
    config = StylesConfig(
        heading=HeadingStyle(align='left'),
    )
    r = Report(config=config)
    r.h1('X')
    r.save(str(docx_path))

    paras = paragraphs_xml(docx_path)
    assert paragraph_alignment(paras[0]) == 'left'


def test_local_align_overrides_global(docx_path):
    config = StylesConfig(
        heading=HeadingStyle(align='left'),
    )
    r = Report(config=config)
    r.h1('X', align='center')
    r.save(str(docx_path))

    paras = paragraphs_xml(docx_path)
    assert paragraph_alignment(paras[0]) == 'center'


def test_heading_overrides_by_level(docx_path):
    config = StylesConfig(
        heading=HeadingStyle(align='left'),
        heading_overrides={2: HeadingStyle(align='center')},
    )
    r = Report(config=config)
    r.h1('One')
    r.h2('Two')
    r.save(str(docx_path))

    paras = paragraphs_xml(docx_path)
    assert paragraph_alignment(paras[0]) == 'left'
    assert paragraph_alignment(paras[1]) == 'center'


def test_title_default_align_is_center(docx_path):
    r = Report()
    r.title('T')
    r.save(str(docx_path))

    paras = paragraphs_xml(docx_path)
    assert paragraph_alignment(paras[0]) == 'center'


# ---------- validation ----------

def test_invalid_align_raises(report):
    with pytest.raises(ValueError, match='align'):
        report.h1('X', align='centre')


@pytest.mark.parametrize(
    'method', ['title', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6'],
)
def test_all_methods_validate_align(report, method):
    with pytest.raises(ValueError):
        getattr(report, method)('X', align='invalid')


# ---------- chaining ----------

def test_heading_methods_return_report(report):
    assert report.h1('X') is report
    assert report.title('X') is report
    assert report.h6('X') is report


def test_heading_chain(report, docx_path):
    report.h1('A').h2('B').h3('C')
    report.save(str(docx_path))

    paras = paragraphs_xml(docx_path)
    texts = [paragraph_text(p) for p in paras]
    assert texts[:3] == ['A', 'B', 'C']