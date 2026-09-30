"""Low-level XML helpers for python-docx features it doesn't expose.

Kept at the package root so both inline/ and mixins/ can import it
without creating cross-package dependencies.
"""
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.opc.constants import RELATIONSHIP_TYPE as RT
from docx.text.paragraph import Paragraph


def add_hyperlink(paragraph: Paragraph, text: str, url: str,
                  color: str = '0563C1') -> None:
    """Append a hyperlink run to the paragraph."""
    r_id = paragraph.part.relate_to(url, RT.HYPERLINK, is_external=True)
    hyperlink = OxmlElement('w:hyperlink')
    hyperlink.set(qn('r:id'), r_id)

    run = OxmlElement('w:r')
    rPr = OxmlElement('w:rPr')

    u = OxmlElement('w:u')
    u.set(qn('w:val'), 'single')
    rPr.append(u)

    c = OxmlElement('w:color')
    c.set(qn('w:val'), color)
    rPr.append(c)

    run.append(rPr)

    t = OxmlElement('w:t')
    t.text = text
    t.set(qn('xml:space'), 'preserve')
    run.append(t)

    hyperlink.append(run)
    paragraph._p.append(hyperlink)


def set_paragraph_shading(paragraph: Paragraph, fill: str) -> None:
    """Set paragraph background color (hex without '#')."""
    pPr = paragraph._p.get_or_add_pPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'), fill)
    pPr.append(shd)


def set_paragraph_bottom_border(paragraph: Paragraph, size: int = 6,
                                 color: str = 'auto') -> None:
    """Draw a horizontal rule as bottom border of the paragraph."""
    pPr = paragraph._p.get_or_add_pPr()
    pBdr = OxmlElement('w:pBdr')
    bottom = OxmlElement('w:bottom')
    bottom.set(qn('w:val'), 'single')
    bottom.set(qn('w:sz'), str(size))
    bottom.set(qn('w:space'), '1')
    bottom.set(qn('w:color'), color)
    pBdr.append(bottom)
    pPr.append(pBdr)


def _add_field(paragraph: Paragraph, instr: str,
               placeholder: str = '', dirty: bool = False) -> None:
    """Append a Word field code (PAGE, TOC, SEQ, ...) to the paragraph.

    `dirty=True` sets w:dirty on the field-begin char, which instructs
    Word to recalculate the field when the document is opened.
    """
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
        t = OxmlElement('w:t')
        t.text = placeholder
        r.append(t)
    r.append(fld_end)


def add_page_number(paragraph: Paragraph) -> None:
    """Insert a PAGE field (updated by Word automatically)."""
    _add_field(paragraph, 'PAGE', '1')


def add_toc(paragraph: Paragraph, levels: str = '1-3',
            dirty: bool = True) -> None:
    """Insert a TOC field.

    If dirty is True, Word updates the TOC automatically when the
    document is opened. LibreOffice honours the same flag for TOC
    fields in recent versions; otherwise use Edit → Update Fields.
    """
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


def set_update_fields_on_open(doc, value: bool = True) -> None:
    """Set w:updateFields in settings.xml so Word refreshes fields on open.

    This is a document-level setting and complements the per-field
    dirty flag. Applied together, they cover both Word and LibreOffice.
    """
    settings = doc.settings.element
    existing = settings.find(qn('w:updateFields'))
    if existing is not None:
        settings.remove(existing)
    el = OxmlElement('w:updateFields')
    el.set(qn('w:val'), 'true' if value else 'false')
    settings.append(el)