"""Tests for CodeMixin — code blocks, styling, alignment."""
from docx_report_gen import Report, StylesConfig, CodeStyle
from docx_report_gen.docx import to_twips

from ._helpers import (
    paragraphs_xml, paragraph_alignment, paragraph_indent,
    paragraph_spacing, paragraph_style_id, paragraph_text, has_shading,
)


# ---------- basics ----------

def test_code_creates_one_paragraph_per_line(report, docx_path):
    report.code('line1\nline2\nline3')
    report.save(str(docx_path))
    paras = paragraphs_xml(docx_path)
    assert len(paras) == 3
    assert paragraph_text(paras[0]) == 'line1'
    assert paragraph_text(paras[1]) == 'line2'
    assert paragraph_text(paras[2]) == 'line3'


def test_code_uses_report_code_style(report, docx_path):
    report.code('x')
    report.save(str(docx_path))
    paras = paragraphs_xml(docx_path)
    assert paragraph_style_id(paras[0]) == 'ReportCode'


def test_code_empty_line_uses_space(report, docx_path):
    report.code('a\n\nb')
    report.save(str(docx_path))
    paras = paragraphs_xml(docx_path)
    assert paragraph_text(paras[1]) == ' '


def test_code_empty_string_creates_one_paragraph(report, docx_path):
    report.code('')
    report.save(str(docx_path))
    paras = paragraphs_xml(docx_path)
    assert len(paras) == 1


def test_code_preserves_leading_whitespace(report, docx_path):
    report.code('def f():\n    return 1')
    report.save(str(docx_path))
    paras = paragraphs_xml(docx_path)
    assert paragraph_text(paras[1]) == '    return 1'


# ---------- styling from config ----------

def test_code_background_shading(docx_path):
    config = StylesConfig(code=CodeStyle(background='EEEEEE'))
    r = Report(config=config)
    r.code('x')
    r.save(str(docx_path))
    paras = paragraphs_xml(docx_path)
    assert has_shading(paras[0]) == 'EEEEEE'


def test_code_empty_background_disables_shading(docx_path):
    """`background=''` (empty string) means no shading.

    None is reserved by the three-level resolve chain to mean
    'not set here, try the next source', so it cannot express
    'explicitly no shading'. Empty string is falsy and skips
    the set_paragraph_shading call in CodeMixin.code().
    """
    config = StylesConfig(code=CodeStyle(background=''))
    r = Report(config=config)
    r.code('x')
    r.save(str(docx_path))
    paras = paragraphs_xml(docx_path)
    assert has_shading(paras[0]) is None


def test_code_line_spacing_from_config(docx_path):
    config = StylesConfig(code=CodeStyle(line_spacing=1.0))
    r = Report(config=config)
    r.code('x')
    r.save(str(docx_path))
    paras = paragraphs_xml(docx_path)
    spacing = paragraph_spacing(paras[0])
    assert spacing.get('line') == 240


# ---------- local overrides ----------

def test_code_local_align(report, docx_path):
    report.code('x', align='center')
    report.save(str(docx_path))
    paras = paragraphs_xml(docx_path)
    assert paragraph_alignment(paras[0]) == 'center'


def test_code_local_left_indent(docx_path):
    r = Report()
    r.code('x', left_indent=1.5)
    r.save(str(docx_path))
    paras = paragraphs_xml(docx_path)
    indent = paragraph_indent(paras[0])
    assert indent.get('left') == to_twips(1.5, 'cm')


# ---------- language argument ----------

def test_code_language_does_not_affect_output(report, docx_path):
    report.code('x = 1', language='python')
    report.save(str(docx_path))
    paras = paragraphs_xml(docx_path)
    assert paragraph_text(paras[0]) == 'x = 1'


# ---------- chaining ----------

def test_code_returns_self(report):
    assert report.code('x') is report