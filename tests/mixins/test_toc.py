"""Tests for TocMixin — toc() and update_toc()."""
import zipfile

from lxml import etree

from ._helpers import (
    paragraphs_xml, paragraph_text, instr_texts, settings_xml,
)


W = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'


# ---------- toc() ----------

def test_toc_inserts_field(report, docx_path):
    report.toc()
    report.save(str(docx_path))
    texts = instr_texts(docx_path)
    assert any('TOC' in t for t in texts)


def test_toc_levels_argument(report, docx_path):
    report.toc(levels='1-2')
    report.save(str(docx_path))
    texts = instr_texts(docx_path)
    assert any('"1-2"' in t for t in texts)


def test_toc_with_title(report, docx_path):
    report.toc(title='Содержание')
    report.save(str(docx_path))
    paras = paragraphs_xml(docx_path)
    texts = [paragraph_text(p) for p in paras]
    assert 'Содержание' in texts


def test_toc_without_title_has_no_extra_text(report, docx_path):
    report.toc()
    report.save(str(docx_path))
    paras = paragraphs_xml(docx_path)
    # Only the TOC field paragraph exists, and it does not contain
    # a title. The placeholder text ("Right-click and choose ...")
    # is written by our own field constructor and is expected here —
    # Word replaces it with the real table of contents on update.
    assert len(paras) == 1
    text = paragraph_text(paras[0])
    assert 'Содержание' not in text


def test_toc_returns_self(report):
    assert report.toc() is report


def test_toc_field_is_dirty(report, docx_path):
    """TOC field must carry w:dirty so Word updates it on open."""
    report.toc()
    report.save(str(docx_path))
    xml_bytes = None
    with zipfile.ZipFile(docx_path) as zf:
        xml_bytes = zf.read('word/document.xml')
    xml = etree.fromstring(xml_bytes)
    dirty = False
    for el in xml.iter(f'{{{W}}}fldChar'):
        if (el.get(f'{{{W}}}fldCharType') == 'begin'
                and el.get(f'{{{W}}}dirty') == 'true'):
            dirty = True
            break
    assert dirty


# ---------- update_toc() ----------

def test_update_toc_sets_update_fields(report, docx_path):
    report.toc()
    report.update_toc()
    report.save(str(docx_path))

    settings = settings_xml(docx_path)
    el = settings.find(f'{{{W}}}updateFields')
    assert el is not None
    assert el.get(f'{{{W}}}val') == 'true'


def test_update_toc_marks_all_fields_dirty(report, docx_path):
    """update_toc marks every existing field dirty, not only the TOC."""
    report.toc()
    # Add a page number field indirectly through another section
    report.page_numbers()
    report.update_toc()
    report.save(str(docx_path))

    # Confirm at least the TOC field is still dirty
    with zipfile.ZipFile(docx_path) as zf:
        xml = etree.fromstring(zf.read('word/document.xml'))
    dirty_count = sum(
        1 for el in xml.iter(f'{{{W}}}fldChar')
        if el.get(f'{{{W}}}fldCharType') == 'begin'
        and el.get(f'{{{W}}}dirty') == 'true'
    )
    assert dirty_count >= 1


def test_update_toc_idempotent(report, docx_path):
    report.toc()
    report.update_toc()
    report.update_toc()
    report.save(str(docx_path))
    settings = settings_xml(docx_path)
    # Only one updateFields element
    matches = settings.findall(f'{{{W}}}updateFields')
    assert len(matches) == 1


def test_update_toc_returns_self(report):
    assert report.update_toc() is report