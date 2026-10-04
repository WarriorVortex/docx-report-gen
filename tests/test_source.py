"""Tests for the source= parameter and set_source / set_document."""
import pytest
from docx import Document
from docx.shared import Pt

from docx_report_gen import Report
from docx_report_gen.docx import DocxDocument


@pytest.fixture
def title_docx(tmp_path):
    """A small .docx with custom content, used as a source."""
    doc = Document()
    p1 = doc.add_paragraph()
    p1.add_run('СПбПУ').bold = True

    p2 = doc.add_paragraph('ЛАБОРАТОРНАЯ РАБОТА №2')
    p2.paragraph_format.line_spacing = Pt(24)

    path = tmp_path / 'title.docx'
    doc.save(str(path))
    return path


# ---------- Report(source=...) ----------

def test_report_accepts_path_string(title_docx):
    r = Report(source=str(title_docx))
    texts = [p.text for p in r.doc.paragraphs if p.text]
    assert 'СПбПУ' in texts
    assert 'ЛАБОРАТОРНАЯ РАБОТА №2' in texts


def test_report_accepts_path_object(title_docx):
    r = Report(source=title_docx)
    texts = [p.text for p in r.doc.paragraphs if p.text]
    assert 'СПбПУ' in texts


def test_report_accepts_document_object():
    src = Document()
    src.add_paragraph('From Document')
    r = Report(source=src)
    texts = [p.text for p in r.doc.paragraphs if p.text]
    assert 'From Document' in texts


def test_report_without_source_is_empty():
    r = Report()
    non_empty = [p.text for p in r.doc.paragraphs if p.text]
    assert non_empty == []


def test_source_preserves_direct_line_spacing(title_docx):
    from docx.oxml.ns import qn

    r = Report(source=title_docx)
    for para in r.doc.paragraphs:
        if para.text == 'ЛАБОРАТОРНАЯ РАБОТА №2':
            pPr = para._p.find(qn('w:pPr'))
            spacing = pPr.find(qn('w:spacing'))
            assert spacing is not None
            assert spacing.get(qn('w:line')) == '480'   # 24pt = 480
            break
    else:
        pytest.fail('paragraph not found')


def test_source_docdefaults_are_preserved(title_docx, tmp_path):
    """The loaded document keeps the source's docDefaults unchanged.

    Both the source and the output are python-docx documents, so both
    carry the same template defaults. The test verifies equality
    rather than assuming a specific value.
    """
    import zipfile
    from lxml import etree

    W = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'

    def read_docdefaults(path):
        with zipfile.ZipFile(path) as zf:
            styles = etree.fromstring(zf.read('word/styles.xml'))
        dd = styles.find(f'{{{W}}}docDefaults')
        if dd is None:
            return None
        return etree.tostring(dd)

    # Read source's docDefaults.
    src_defaults = read_docdefaults(title_docx)

    # Load and save through Report.
    r = Report(source=title_docx)
    out_path = tmp_path / 'out.docx'
    r.save(str(out_path))

    out_defaults = read_docdefaults(out_path)

    # Same element, byte for byte (lxml serialization is deterministic
    # for the same tree structure).
    assert src_defaults == out_defaults


def test_user_content_after_source(title_docx):
    r = Report(source=title_docx)
    r.h1('Введение')
    r.p('Основной текст.')

    texts = [p.text for p in r.doc.paragraphs if p.text]
    assert texts.index('СПбПУ') < texts.index('Введение')


# ---------- set_source ----------

def test_set_source_replaces_document(title_docx):
    r = Report()
    r.h1('Before')
    r.set_source(title_docx)

    texts = [p.text for p in r.doc.paragraphs if p.text]
    assert 'СПбПУ' in texts
    assert 'Before' not in texts


def test_set_source_returns_report(title_docx):
    r = Report()
    assert r.set_source(title_docx) is r


def test_set_source_chains(title_docx):
    r = Report()
    r.set_source(title_docx).h1('After')
    texts = [p.text for p in r.doc.paragraphs if p.text]
    assert 'СПбПУ' in texts
    assert 'After' in texts


def test_set_source_missing_file(tmp_path):
    r = Report()
    with pytest.raises(FileNotFoundError):
        r.set_source(tmp_path / 'nope.docx')


def test_set_source_resets_counters(title_docx):
    """After set_source, formula counter starts from zero."""
    r = Report()
    r.f('x^2', number=True)
    r.f('y^2', number=True)
    r.set_source(title_docx)
    r.f('z^2', number=True)
    text = r.doc.paragraphs[-1].text
    assert '(1)' in text


# ---------- set_document ----------

def test_set_document_replaces():
    src = Document()
    src.add_paragraph('From Document')
    r = Report()
    r.h1('Before')
    r.set_document(src)

    texts = [p.text for p in r.doc.paragraphs if p.text]
    assert 'From Document' in texts
    assert 'Before' not in texts


def test_set_document_returns_report():
    src = Document()
    r = Report()
    assert r.set_document(src) is r


def test_set_document_without_apply_styles():
    src = Document()
    src.styles['Normal'].font.name = 'Arial'

    r = Report()
    r.set_document(src, apply_styles=False)
    assert r.doc.styles['Normal'].font.name == 'Arial'


def test_set_document_with_apply_styles():
    src = Document()
    src.styles['Normal'].font.name = 'Arial'

    r = Report()
    r.set_document(src, apply_styles=True)
    # Report's default font (Times New Roman) is applied.
    assert r.doc.styles['Normal'].font.name == 'Times New Roman'


def test_set_document_accepts_docx_document_type():
    src = Document()
    r = Report()
    # Same type assertion as user code would do.
    assert isinstance(src, DocxDocument)
    r.set_document(src)