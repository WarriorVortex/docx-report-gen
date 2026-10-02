"""Tests for inline nodes — XML output, validation, factory types.

python-docx can open a document and read paragraph text, but it does
not expose OMML, field codes or hyperlink relationships. Those checks
unpack the saved .docx and inspect word/document.xml directly.
"""
import zipfile

import pytest
from docx import Document
from docx.enum.text import WD_COLOR_INDEX
from lxml import etree

from docx_report_gen import (
    b, i, u, s, sup, sub, color, highlight, f, link, ref,
)
from docx_report_gen.inline import (
    Bold, Italic, Underline, Strike, Sup, Sub, Color, Highlight,
    Formula, Link, Reference, Inline,
)


W = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
M = 'http://schemas.openxmlformats.org/officeDocument/2006/math'
R = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'
PKG_REL = 'http://schemas.openxmlformats.org/package/2006/relationships'


# ---------- helpers ----------

def _document_xml(path):
    with zipfile.ZipFile(path) as zf:
        return etree.fromstring(zf.read('word/document.xml'))


def _rels_xml(path):
    with zipfile.ZipFile(path) as zf:
        return etree.fromstring(zf.read('word/_rels/document.xml.rels'))


def _run_props(path):
    """Return a list of tag-name lists, one per run in document order.

    Every entry describes the children of the run's <w:rPr> element.
    An empty list means the run has no formatting.
    """
    xml = _document_xml(path)
    result = []
    for run in xml.findall(f'.//{{{W}}}r'):
        r_pr = run.find(f'{{{W}}}rPr')
        if r_pr is None:
            result.append([])
        else:
            result.append(
                [etree.QName(child).localname for child in r_pr]
            )
    return result


def _text_runs(path):
    """Return (text, props) pairs for runs that carry a w:t element."""
    xml = _document_xml(path)
    pairs = []
    for run in xml.findall(f'.//{{{W}}}r'):
        t = run.find(f'{{{W}}}t')
        if t is None:
            continue
        r_pr = run.find(f'{{{W}}}rPr')
        props = (
            [etree.QName(c).localname for c in r_pr]
            if r_pr is not None else []
        )
        pairs.append((t.text or '', props))
    return pairs


def _find_attr_in_rpr(path, tag_local, attr_local):
    """Return the value of an attribute on the first matching rPr child."""
    xml = _document_xml(path)
    for el in xml.iter(f'{{{W}}}{tag_local}'):
        value = el.get(f'{{{W}}}{attr_local}')
        if value is not None:
            return value
    return None


# ---------- factory types ----------

def test_factories_return_inline_instances():
    assert isinstance(b('x'), Bold)
    assert isinstance(i('x'), Italic)
    assert isinstance(u('x'), Underline)
    assert isinstance(s('x'), Strike)
    assert isinstance(sup('x'), Sup)
    assert isinstance(sub('x'), Sub)
    assert isinstance(color('x', (0, 0, 0)), Color)
    assert isinstance(highlight('x'), Highlight)
    assert isinstance(f('x^2'), Formula)
    assert isinstance(link('text', 'https://e.com'), Link)
    assert isinstance(ref('name'), Reference)


def test_all_factories_produce_inline_subclasses():
    for node in (
        b('x'), i('x'), u('x'), s('x'), sup('x'), sub('x'),
        color('x', (0, 0, 0)), highlight('x'), f('x'), ref('x'),
    ):
        assert isinstance(node, Inline)


# ---------- simple text run properties ----------

def test_bold_emits_w_b(report, docx_path):
    report.p(b('bold'))
    report.save(str(docx_path))
    props = _run_props(docx_path)
    assert 'b' in props[0]


def test_italic_emits_w_i(report, docx_path):
    report.p(i('italic'))
    report.save(str(docx_path))
    props = _run_props(docx_path)
    assert 'i' in props[0]


def test_underline_emits_w_u(report, docx_path):
    report.p(u('underlined'))
    report.save(str(docx_path))
    props = _run_props(docx_path)
    assert 'u' in props[0]
    assert _find_attr_in_rpr(docx_path, 'u', 'val') == 'single'


def test_strike_emits_w_strike(report, docx_path):
    report.p(s('struck'))
    report.save(str(docx_path))
    props = _run_props(docx_path)
    assert 'strike' in props[0]


def test_superscript_emits_vert_align(report, docx_path):
    report.p(sup('2'))
    report.save(str(docx_path))
    props = _run_props(docx_path)
    assert 'vertAlign' in props[0]
    assert _find_attr_in_rpr(docx_path, 'vertAlign', 'val') == 'superscript'


def test_subscript_emits_vert_align(report, docx_path):
    report.p(sub('2'))
    report.save(str(docx_path))
    props = _run_props(docx_path)
    assert 'vertAlign' in props[0]
    assert _find_attr_in_rpr(docx_path, 'vertAlign', 'val') == 'subscript'


def test_color_emits_w_color_with_rgb(report, docx_path):
    report.p(color('red', (255, 0, 0)))
    report.save(str(docx_path))
    props = _run_props(docx_path)
    assert 'color' in props[0]
    assert _find_attr_in_rpr(docx_path, 'color', 'val') == 'FF0000'


def test_color_lowercase_rgb_formatted_uppercase(report, docx_path):
    report.p(color('x', (10, 20, 30)))
    report.save(str(docx_path))
    assert _find_attr_in_rpr(docx_path, 'color', 'val') == '0A141E'


# ---------- highlight ----------

def test_highlight_default_is_yellow(report, docx_path):
    report.p(highlight('x'))
    report.save(str(docx_path))
    props = _run_props(docx_path)
    assert 'highlight' in props[0]
    assert _find_attr_in_rpr(docx_path, 'highlight', 'val') == 'yellow'


@pytest.mark.parametrize('name,wml', [
    # Bright primary names — the WML value IS the user-facing name.
    ('yellow', 'yellow'),
    ('green', 'green'),          # BRIGHT_GREEN
    ('cyan', 'cyan'),            # TURQUOISE
    ('magenta', 'magenta'),      # PINK
    ('blue', 'blue'),
    ('red', 'red'),
    # Dark variants.
    ('darkGreen', 'darkGreen'),  # GREEN
    ('darkBlue', 'darkBlue'),
    ('darkRed', 'darkRed'),
    ('darkYellow', 'darkYellow'),
    ('darkCyan', 'darkCyan'),    # TEAL
    ('darkMagenta', 'darkMagenta'),
    # Grays.
    ('lightGray', 'lightGray'),  # GRAY_25
    ('darkGray', 'darkGray'),    # GRAY_50
    # Extremes.
    ('black', 'black'),
    ('white', 'white'),
])
def test_highlight_named_colors(report, docx_path, name, wml):
    report.p(highlight('x', name))
    report.save(str(docx_path))
    assert _find_attr_in_rpr(docx_path, 'highlight', 'val') == wml


def test_highlight_accepts_wd_color_index():
    node = highlight('x', WD_COLOR_INDEX.BRIGHT_GREEN)
    assert node.color == WD_COLOR_INDEX.BRIGHT_GREEN


def test_highlight_enum_member_renders_correctly(report, docx_path):
    report.p(highlight('x', WD_COLOR_INDEX.TURQUOISE))
    report.save(str(docx_path))
    assert _find_attr_in_rpr(docx_path, 'highlight', 'val') == 'cyan'


def test_highlight_unknown_color_raises():
    with pytest.raises(ValueError, match='unknown highlight color'):
        highlight('x', 'pink')


def test_highlight_case_sensitive_wml_names():
    """'LIGHTGRAY' is not a valid WML name; only 'lightGray' is."""
    with pytest.raises(ValueError):
        highlight('x', 'LIGHTGRAY')


# ---------- formula ----------

def test_formula_emits_omml(report, docx_path):
    report.p('before ', f('E = mc^2'), ' after')
    report.save(str(docx_path))
    xml = _document_xml(docx_path)
    omaths = xml.findall(f'.//{{{M}}}oMath')
    assert len(omaths) == 1


def test_two_formulas_produce_two_omath_elements(report, docx_path):
    report.p(f('a'), ' ', f('b'))
    report.save(str(docx_path))
    xml = _document_xml(docx_path)
    omaths = xml.findall(f'.//{{{M}}}oMath')
    assert len(omaths) == 2


# ---------- hyperlink ----------

def test_link_emits_hyperlink_element(report, docx_path):
    report.p(link('click', 'https://example.com'))
    report.save(str(docx_path))
    xml = _document_xml(docx_path)
    hyperlinks = xml.findall(f'.//{{{W}}}hyperlink')
    assert len(hyperlinks) == 1


def test_link_has_r_id_attribute(report, docx_path):
    report.p(link('click', 'https://example.com'))
    report.save(str(docx_path))
    xml = _document_xml(docx_path)
    hl = xml.find(f'.//{{{W}}}hyperlink')
    assert hl is not None
    assert hl.get(f'{{{R}}}id') is not None


def test_link_creates_external_relationship(report, docx_path):
    report.p(link('click', 'https://example.com/path'))
    report.save(str(docx_path))
    rels = _rels_xml(docx_path)

    hyperlink_type = (
        'http://schemas.openxmlformats.org/officeDocument/2006'
        '/relationships/hyperlink'
    )
    matches = [
        rel for rel in rels.findall(f'{{{PKG_REL}}}Relationship')
        if rel.get('Type') == hyperlink_type
    ]
    assert len(matches) == 1
    assert matches[0].get('Target') == 'https://example.com/path'
    assert matches[0].get('TargetMode') == 'External'


def test_link_visible_text_inside_hyperlink(report, docx_path):
    report.p(link('described', 'https://example.com'))
    report.save(str(docx_path))
    xml = _document_xml(docx_path)
    hl = xml.find(f'.//{{{W}}}hyperlink')
    text_el = hl.find(f'.//{{{W}}}t')
    assert text_el is not None
    assert text_el.text == 'described'


# ---------- reference ----------

def test_ref_requires_non_empty_name():
    with pytest.raises(ValueError):
        ref('')


def test_ref_rejects_whitespace():
    with pytest.raises(ValueError):
        ref('has space')


def test_ref_emits_instr_text(report, docx_path):
    report.p('see ', ref('results'))
    report.save(str(docx_path))
    xml = _document_xml(docx_path)
    instr_texts = [
        el.text or '' for el in xml.findall(f'.//{{{W}}}instrText')
    ]
    assert any('REF _Ref_results' in t for t in instr_texts)


def test_ref_instr_contains_hyperlink_flag(report, docx_path):
    report.p(ref('data'))
    report.save(str(docx_path))
    xml = _document_xml(docx_path)
    instr_texts = [el.text or '' for el in xml.findall(f'.//{{{W}}}instrText')]
    assert any('\\h' in t for t in instr_texts)


def test_ref_field_has_dirty_flag(report, docx_path):
    report.p(ref('data'))
    report.save(str(docx_path))
    xml = _document_xml(docx_path)
    begins = xml.findall(f'.//{{{W}}}fldChar')
    dirty = [
        el for el in begins
        if el.get(f'{{{W}}}fldCharType') == 'begin'
        and el.get(f'{{{W}}}dirty') == 'true'
    ]
    assert dirty, 'REF field begin must carry w:dirty="true"'


# ---------- mixing ----------

def test_multiple_nodes_in_one_paragraph(report, docx_path):
    report.p(
        'plain ',
        b('bold'),
        ' ',
        i('italic'),
        ' ',
        u('under'),
        ' ',
        f('x^2'),
        ' ',
        color('red', (255, 0, 0)),
    )
    report.save(str(docx_path))

    pairs = _text_runs(docx_path)
    texts = [t for t, _ in pairs]
    assert 'plain ' in texts
    assert 'bold' in texts
    assert 'italic' in texts
    assert 'under' in texts
    assert 'red' in texts

    xml = _document_xml(docx_path)
    assert xml.find(f'.//{{{M}}}oMath') is not None


def test_multiple_links_get_distinct_relationship_ids(report, docx_path):
    report.p(link('a', 'https://a.example'), ' ', link('b', 'https://b.example'))
    report.save(str(docx_path))

    xml = _document_xml(docx_path)
    ids = [
        hl.get(f'{{{R}}}id')
        for hl in xml.findall(f'.//{{{W}}}hyperlink')
    ]
    assert len(ids) == 2
    assert ids[0] != ids[1]


def test_empty_text_node_still_creates_run(report, docx_path):
    report.p(b(''))
    report.save(str(docx_path))
    props = _run_props(docx_path)
    assert 'b' in props[0]


def test_nodes_survive_save_and_reopen(report, docx_path):
    report.p(b('bold text'))
    report.save(str(docx_path))

    doc = Document(str(docx_path))
    texts = [p.text for p in doc.paragraphs]
    assert 'bold text' in texts


def test_nested_formatting_in_separate_runs(report, docx_path):
    """Two adjacent inline nodes become two separate runs."""
    report.p(b('bold'), i('italic'))
    report.save(str(docx_path))

    pairs = _text_runs(docx_path)
    assert len(pairs) == 2
    assert pairs[0][0] == 'bold'
    assert 'b' in pairs[0][1]
    assert pairs[1][0] == 'italic'
    assert 'i' in pairs[1][1]