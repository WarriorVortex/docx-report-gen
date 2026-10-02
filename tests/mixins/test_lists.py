"""Tests for ListMixin — ul, ol, nesting."""
from docx_report_gen import Report

from ._helpers import (
    paragraphs_xml, paragraph_alignment, paragraph_style_id, paragraph_text,
)


# ---------- ul ----------

def test_ul_creates_bullet_paragraphs(report, docx_path):
    report.ul(['first', 'second', 'third'])
    report.save(str(docx_path))
    paras = paragraphs_xml(docx_path)
    assert len(paras) == 3
    assert paragraph_text(paras[0]) == 'first'
    assert paragraph_text(paras[1]) == 'second'
    assert paragraph_text(paras[2]) == 'third'


def test_ul_uses_list_bullet_style(report, docx_path):
    report.ul(['a'])
    report.save(str(docx_path))
    paras = paragraphs_xml(docx_path)
    style = paragraph_style_id(paras[0])
    assert style in ('ListBullet', 'List Bullet')


# ---------- ol ----------

def test_ol_creates_numbered_paragraphs(report, docx_path):
    report.ol(['one', 'two'])
    report.save(str(docx_path))
    paras = paragraphs_xml(docx_path)
    assert len(paras) == 2
    style = paragraph_style_id(paras[0])
    assert style in ('ListNumber', 'List Number')


# ---------- nesting ----------

def test_nested_list_creates_deeper_style(report, docx_path):
    report.ul(['a', ['nested1', 'nested2'], 'b'])
    report.save(str(docx_path))
    paras = paragraphs_xml(docx_path)
    # 4 paragraphs: a, nested1, nested2, b
    assert len(paras) == 4
    assert paragraph_text(paras[1]) == 'nested1'
    style = paragraph_style_id(paras[1])
    assert style in ('ListBullet2', 'List Bullet 2')


def test_three_level_nesting(report, docx_path):
    report.ul(['a', ['b', ['c']], 'd'])
    report.save(str(docx_path))
    paras = paragraphs_xml(docx_path)
    assert len(paras) == 4


def test_fourth_level_is_silently_ignored(report, docx_path):
    """Beyond level 3, Word has no built-in style; the list does not grow."""
    report.ul(['a', ['b', ['c', ['too_deep']]]])
    report.save(str(docx_path))
    paras = paragraphs_xml(docx_path)
    texts = [paragraph_text(p) for p in paras]
    assert 'too_deep' not in texts


# ---------- alignment resolution ----------

def test_ul_local_align(docx_path):
    r = Report()
    r.ul(['a'], align='center')
    r.save(str(docx_path))
    paras = paragraphs_xml(docx_path)
    assert paragraph_alignment(paras[0]) == 'center'


# ---------- chaining ----------

def test_ul_returns_self(report):
    assert report.ul(['a']) is report


def test_ol_returns_self(report):
    assert report.ol(['a']) is report


# ---------- mixed content ----------

def test_ul_then_paragraph(report, docx_path):
    report.ul(['a', 'b'])
    report.p('after')
    report.save(str(docx_path))
    paras = paragraphs_xml(docx_path)
    assert len(paras) == 3
    assert paragraph_text(paras[2]) == 'after'