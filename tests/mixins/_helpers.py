"""Shared helpers for mixin tests that need to inspect raw XML."""
import zipfile

from lxml import etree


W = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'


# ---------- document.xml access ----------

def document_xml(path):
    with zipfile.ZipFile(path) as zf:
        return etree.fromstring(zf.read('word/document.xml'))


def settings_xml(path):
    with zipfile.ZipFile(path) as zf:
        return etree.fromstring(zf.read('word/settings.xml'))


def paragraphs_xml(path):
    xml = document_xml(path)
    body = xml.find(f'{{{W}}}body')
    return body.findall(f'{{{W}}}p')


def tables_xml(path):
    xml = document_xml(path)
    body = xml.find(f'{{{W}}}body')
    return body.findall(f'{{{W}}}tbl')


# ---------- paragraph inspection ----------

def paragraph_text(elem):
    return ''.join(t.text or '' for t in elem.iter(f'{{{W}}}t'))


def paragraph_style_id(elem):
    p_pr = elem.find(f'{{{W}}}pPr')
    if p_pr is None:
        return None
    style = p_pr.find(f'{{{W}}}pStyle')
    if style is None:
        return None
    return style.get(f'{{{W}}}val')


def paragraph_alignment(elem):
    p_pr = elem.find(f'{{{W}}}pPr')
    if p_pr is None:
        return None
    jc = p_pr.find(f'{{{W}}}jc')
    if jc is None:
        return None
    return jc.get(f'{{{W}}}val')


def paragraph_spacing(elem):
    p_pr = elem.find(f'{{{W}}}pPr')
    if p_pr is None:
        return {}
    spacing = p_pr.find(f'{{{W}}}spacing')
    if spacing is None:
        return {}
    result = {}
    for attr in ('before', 'after', 'line'):
        val = spacing.get(f'{{{W}}}{attr}')
        if val is not None:
            result[attr] = int(val)
    return result


def paragraph_indent(elem):
    p_pr = elem.find(f'{{{W}}}pPr')
    if p_pr is None:
        return {}
    ind = p_pr.find(f'{{{W}}}ind')
    if ind is None:
        return {}
    result = {}
    for attr in ('firstLine', 'left', 'right'):
        val = ind.get(f'{{{W}}}{attr}')
        if val is not None:
            result[attr] = int(val)
    return result


def paragraph_tab_stops(elem):
    p_pr = elem.find(f'{{{W}}}pPr')
    if p_pr is None:
        return []
    tabs = p_pr.find(f'{{{W}}}tabs')
    if tabs is None:
        return []
    result = []
    for tab in tabs.findall(f'{{{W}}}tab'):
        pos = tab.get(f'{{{W}}}pos')
        val = tab.get(f'{{{W}}}val')
        result.append((int(pos) if pos else None, val))
    return result


def has_shading(elem):
    p_pr = elem.find(f'{{{W}}}pPr')
    if p_pr is None:
        return None
    shd = p_pr.find(f'{{{W}}}shd')
    if shd is None:
        return None
    return shd.get(f'{{{W}}}fill')


def has_bottom_border(elem):
    p_pr = elem.find(f'{{{W}}}pPr')
    if p_pr is None:
        return False
    p_bdr = p_pr.find(f'{{{W}}}pBdr')
    if p_bdr is None:
        return False
    return p_bdr.find(f'{{{W}}}bottom') is not None


def has_page_break(path):
    xml = document_xml(path)
    for br in xml.iter(f'{{{W}}}br'):
        if br.get(f'{{{W}}}type') == 'page':
            return True
    return False


# ---------- fields, bookmarks ----------

def instr_texts(path):
    xml = document_xml(path)
    return [el.text or '' for el in xml.findall(f'.//{{{W}}}instrText')]


def bookmark_names(path):
    xml = document_xml(path)
    result = []
    for el in xml.findall(f'.//{{{W}}}bookmarkStart'):
        name = el.get(f'{{{W}}}name')
        if name:
            result.append(name)
    return result


def has_field_in_part(part_xml_bytes, field_substring):
    xml = etree.fromstring(part_xml_bytes)
    for el in xml.iter(f'{{{W}}}instrText'):
        if field_substring in (el.text or ''):
            return True
    return False


# ---------- table inspection ----------

def row_grid_spans(tbl, row_idx):
    """Return the list of gridSpan values for a given row (1 if absent)."""
    rows = tbl.findall(f'{{{W}}}tr')
    row = rows[row_idx]
    result = []
    for tc in row.findall(f'{{{W}}}tc'):
        tc_pr = tc.find(f'{{{W}}}tcPr')
        gs = None
        if tc_pr is not None:
            gs = tc_pr.find(f'{{{W}}}gridSpan')
        result.append(int(gs.get(f'{{{W}}}val')) if gs is not None else 1)
    return result


def cell_widths_cm_twips(path, table_idx=0):
    """Return tcW values (in twips) for cells of the first row."""
    xml = document_xml(path)
    body = xml.find(f'{{{W}}}body')
    tables = body.findall(f'{{{W}}}tbl')
    tbl = tables[table_idx]
    rows = tbl.findall(f'{{{W}}}tr')
    result = []
    for tc in rows[0].findall(f'{{{W}}}tc'):
        tc_pr = tc.find(f'{{{W}}}tcPr')
        tc_w = None
        if tc_pr is not None:
            tc_w_el = tc_pr.find(f'{{{W}}}tcW')
            if tc_w_el is not None:
                tc_w = int(tc_w_el.get(f'{{{W}}}w'))
        result.append(tc_w)
    return result