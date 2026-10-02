"""Tests for ImageMixin — insertion, width, caption, bookmark."""
import pytest

from docx import Document
from docx.shared import Cm

from docx_report_gen import Report

from ._helpers import (
    paragraphs_xml, paragraph_text, instr_texts, bookmark_names,
)


# ---------- insertion ----------

def test_img_inserts_one_shape(report, png_image, docx_path):
    report.img(png_image)
    report.save(str(docx_path))

    doc = Document(str(docx_path))
    assert len(doc.inline_shapes) == 1


def test_img_returns_self(report, png_image):
    assert report.img(png_image) is report


def test_multiple_images(report, png_image, docx_path):
    report.img(png_image)
    report.img(png_image)
    report.save(str(docx_path))

    doc = Document(str(docx_path))
    assert len(doc.inline_shapes) == 2


# ---------- width ----------

def test_img_default_width_is_native(report, png_image, docx_path):
    report.img(png_image)
    report.save(str(docx_path))

    doc = Document(str(docx_path))
    # 1x1 PNG native size is very small; just ensure it's present
    assert doc.inline_shapes[0].width > 0


def test_img_width_in_cm(report, png_image, docx_path):
    report.img(png_image, width=4.0)
    report.save(str(docx_path))

    doc = Document(str(docx_path))
    assert doc.inline_shapes[0].width == Cm(4.0)


def test_img_width_as_length_object(report, png_image, docx_path):
    from docx.shared import Inches
    report.img(png_image, width=Inches(1.0))
    report.save(str(docx_path))

    doc = Document(str(docx_path))
    assert doc.inline_shapes[0].width == Inches(1.0)


# ---------- caption ----------

def test_img_caption_creates_paragraph(report, png_image, docx_path):
    report.img(png_image, caption='Рисунок')
    report.save(str(docx_path))

    paras = paragraphs_xml(docx_path)
    texts = [paragraph_text(p) for p in paras]
    assert any('Рисунок' in t for t in texts)


def test_img_caption_has_seq_field(report, png_image, docx_path):
    report.img(png_image, caption='Рисунок')
    report.save(str(docx_path))
    assert any('SEQ Figure' in t for t in instr_texts(docx_path))


def test_img_without_caption_has_no_seq(report, png_image, docx_path):
    report.img(png_image)
    report.save(str(docx_path))
    assert not any('SEQ Figure' in t for t in instr_texts(docx_path))


# ---------- bookmark via name ----------

def test_img_name_creates_bookmark(report, png_image, docx_path):
    report.img(png_image, caption='Рисунок', name='plot')
    report.save(str(docx_path))
    assert '_Ref_plot' in bookmark_names(docx_path)


# ---------- alignment ----------

def test_img_default_align_from_config(docx_path, png_image):
    r = Report()
    r.img(png_image, align='center')
    r.save(str(docx_path))

    paras = paragraphs_xml(docx_path)
    # First paragraph holds the image
    from ._helpers import paragraph_alignment
    assert paragraph_alignment(paras[0]) == 'center'


def test_img_invalid_align_raises(report, png_image):
    with pytest.raises(ValueError):
        report.img(png_image, align='centre')


# ---------- file existence ----------

def test_img_missing_file_raises(report, tmp_path):
    missing = tmp_path / 'nope.png'
    with pytest.raises(FileNotFoundError):
        report.img(str(missing))


# ---------- caption alignment ----------

def test_img_caption_align_local(report, png_image, docx_path):
    from ._helpers import paragraph_alignment
    report.img(png_image, caption='X', caption_align='left')
    report.save(str(docx_path))

    paras = paragraphs_xml(docx_path)
    # Caption is the second paragraph (first is the image)
    assert paragraph_alignment(paras[1]) == 'left'