"""Title style must be created if missing in the document."""
from docx import Document

from docx_report_gen.styles import StylesConfig, apply


def test_apply_creates_missing_title_style():
    doc = Document()
    # Simulate a minimal .docx: remove the Title style.
    for style in list(doc.styles):
        if style.name == 'Title':
            style.element.getparent().remove(style.element)
            break

    # Should not raise.
    apply(doc, StylesConfig())

    # Style is now present.
    names = {s.name for s in doc.styles}
    assert 'Title' in names


def test_apply_creates_missing_heading_styles():
    doc = Document()
    for style in list(doc.styles):
        if style.name and style.name.startswith('Heading'):
            style.element.getparent().remove(style.element)

    apply(doc, StylesConfig())

    names = {s.name for s in doc.styles}
    assert 'Heading 1' in names
    assert 'Heading 2' in names