# mypy: disable-error-code="no-untyped-call"
"""Low-level helpers around python-docx that would otherwise be untyped.

python-docx ships without a py.typed marker, and its public API has no
type information visible to mypy. This module is the single place where
calls into the library happen directly. Every function here re-exports
a small, typed surface: parameters and return values are annotated, and
callers in the rest of the package use these wrappers instead of
touching python-docx methods that mypy treats as untyped.

The module-level directive above disables no-untyped-call for this file
only. Everywhere else in the package the check remains enabled, so any
new direct call to an untyped python-docx method outside this module
will be flagged.

Naming: the leading underscore marks the module as private to the
package. It is not part of the public API and is not re-exported from
docx_report_gen.__init__.
"""
# python-docx does not expose public APIs for paragraph/run XML elements.
# Accessing `._p`, `._r` and `._element` is the intended way to reach the
# underlying XML; there is no public alternative.
# pylint: disable=protected-access
from typing import Any

from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.opc.constants import RELATIONSHIP_TYPE as RT
from docx.text.paragraph import Paragraph

from ._docx import DocxDocument


def add_page_break(doc: DocxDocument) -> None:
    """Append a page break to the document."""
    doc.add_page_break()


def add_hyperlink(paragraph: Paragraph, text: str, url: str,
                  color: str = '0563C1') -> None:
    """Append a hyperlink run to the paragraph."""
    r_id = paragraph.part.relate_to(url, RT.HYPERLINK, is_external=True)
    hyperlink = OxmlElement('w:hyperlink')
    hyperlink.set(qn('r:id'), r_id)

    run = OxmlElement('w:r')
    r_pr = OxmlElement('w:rPr')

    underline = OxmlElement('w:u')
    underline.set(qn('w:val'), 'single')
    r_pr.append(underline)

    color_el = OxmlElement('w:color')
    color_el.set(qn('w:val'), color)
    r_pr.append(color_el)

    run.append(r_pr)

    text_el = OxmlElement('w:t')
    text_el.text = text
    text_el.set(qn('xml:space'), 'preserve')
    run.append(text_el)

    hyperlink.append(run)
    paragraph._p.append(hyperlink)


def set_paragraph_shading(paragraph: Paragraph, fill: str) -> None:
    """Set paragraph background color (hex without '#')."""
    p_pr = paragraph._p.get_or_add_pPr()
    shading = OxmlElement('w:shd')
    shading.set(qn('w:val'), 'clear')
    shading.set(qn('w:color'), 'auto')
    shading.set(qn('w:fill'), fill)
    p_pr.append(shading)


def set_paragraph_bottom_border(paragraph: Paragraph,
                                 size: int = 6,
                                 color: str = 'auto') -> None:
    """Draw a horizontal rule as bottom border of the paragraph."""
    p_pr = paragraph._p.get_or_add_pPr()
    p_bdr = OxmlElement('w:pBdr')
    bottom = OxmlElement('w:bottom')
    bottom.set(qn('w:val'), 'single')
    bottom.set(qn('w:sz'), str(size))
    bottom.set(qn('w:space'), '1')
    bottom.set(qn('w:color'), color)
    p_bdr.append(bottom)
    p_pr.append(p_bdr)


def clear_cell_content(cell: Any) -> None:
    """Remove every paragraph from a cell."""
    for para in list(cell.paragraphs):
        para._element.getparent().remove(para._element)


def _add_field(paragraph: Paragraph, instr: str,
               placeholder: str = '', dirty: bool = False) -> None:
    """Append a Word field code (PAGE, TOC, SEQ, REF, ...) to the paragraph."""
    run = paragraph.add_run()
    r = run._r

    fld_begin = OxmlElement('w:fldChar')
    fld_begin.set(qn('w:fldCharType'), 'begin')
    if dirty:
        fld_begin.set(qn('w:dirty'), 'true')

    instr_el = OxmlElement('w:instrText')
    instr_el.set(qn('xml:space'), 'preserve')
    instr_el.text = f' {instr} '

    fld_sep = OxmlElement('w:fldChar')
    fld_sep.set(qn('w:fldCharType'), 'separate')

    fld_end = OxmlElement('w:fldChar')
    fld_end.set(qn('w:fldCharType'), 'end')

    r.append(fld_begin)
    r.append(instr_el)
    r.append(fld_sep)
    if placeholder:
        text_el = OxmlElement('w:t')
        text_el.text = placeholder
        r.append(text_el)
    r.append(fld_end)


def add_page_number(paragraph: Paragraph) -> None:
    """Insert a PAGE field (updated by Word automatically)."""
    _add_field(paragraph, 'PAGE', '1')


def add_toc(paragraph: Paragraph, levels: str = '1-3',
            dirty: bool = True) -> None:
    """Insert a TOC field."""
    _add_field(
        paragraph,
        f'TOC \\o "{levels}" \\h \\z \\u',
        'Right-click and choose "Update Field".',
        dirty=dirty,
    )


def mark_fields_dirty(paragraph: Paragraph) -> None:
    """Set w:dirty="true" on every field-begin char in the paragraph."""
    for run in paragraph.runs:
        for fld in run._r.findall(qn('w:fldChar')):
            if fld.get(qn('w:fldCharType')) == 'begin':
                fld.set(qn('w:dirty'), 'true')


def set_update_fields_on_open(doc: DocxDocument,
                              value: bool = True) -> None:
    """Set w:updateFields in settings.xml so Word refreshes fields on open."""
    settings = doc.settings.element
    existing = settings.find(qn('w:updateFields'))
    if existing is not None:
        settings.remove(existing)
    el = OxmlElement('w:updateFields')
    el.set(qn('w:val'), 'true' if value else 'false')
    settings.append(el)


# ---------- bookmarks and cross-reference fields ----------

def add_bookmark_start(paragraph: Paragraph, name: str,
                       bookmark_id: int) -> None:
    """Open a bookmark range at the end of the paragraph."""
    el = OxmlElement('w:bookmarkStart')
    el.set(qn('w:id'), str(bookmark_id))
    el.set(qn('w:name'), name)
    paragraph._p.append(el)


def add_bookmark_end(paragraph: Paragraph, bookmark_id: int) -> None:
    """Close a bookmark range previously opened with add_bookmark_start."""
    el = OxmlElement('w:bookmarkEnd')
    el.set(qn('w:id'), str(bookmark_id))
    paragraph._p.append(el)


def add_seq_field(paragraph: Paragraph, seq_name: str) -> None:
    """Insert a SEQ field — Word's per-name auto-increment counter."""
    _add_field(
        paragraph,
        f'SEQ {seq_name} \\* ARABIC',
        '1',
        dirty=True,
    )


def add_ref_field(paragraph: Paragraph, bookmark_name: str) -> None:
    """Insert a REF field pointing at a bookmark."""
    _add_field(
        paragraph,
        f'REF {bookmark_name} \\h',
        '1',
        dirty=True,
    )