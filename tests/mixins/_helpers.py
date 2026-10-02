"""Shared helpers for mixin tests that need to inspect raw XML."""
import zipfile

from lxml import etree


W = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'


def document_xml(path):
    with zipfile.ZipFile(path) as zf:
        return etree.fromstring(zf.read('word/document.xml'))


def paragraphs_xml(path):
    """Return a list of <w:p> elements from word/document.xml."""
    xml = document_xml(path)
    body = xml.find(f'{{{W}}}body')
    return body.findall(f'{{{W}}}p')


def paragraph_text(elem):
    """Concatenate all w:t text inside a paragraph element."""
    return ''.join(t.text or '' for t in elem.iter(f'{{{W}}}t'))


def paragraph_style_id(elem):
    """Return the style id applied to a paragraph, or None."""
    p_pr = elem.find(f'{{{W}}}pPr')
    if p_pr is None:
        return None
    style = p_pr.find(f'{{{W}}}pStyle')
    if style is None:
        return None
    return style.get(f'{{{W}}}val')


def paragraph_alignment(elem):
    """Return the paragraph's alignment value, or None."""
    p_pr = elem.find(f'{{{W}}}pPr')
    if p_pr is None:
        return None
    jc = p_pr.find(f'{{{W}}}jc')
    if jc is None:
        return None
    return jc.get(f'{{{W}}}val')


def paragraph_spacing(elem):
    """Return a dict of spacing attributes (before, after, line)."""
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
    """Return a dict of indent attributes (firstLine, left, etc.)."""
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
    """Return a list of (position, alignment) tab stops in the paragraph."""
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
    """Return the paragraph's shading fill color, or None."""
    p_pr = elem.find(f'{{{W}}}pPr')
    if p_pr is None:
        return None
    shd = p_pr.find(f'{{{W}}}shd')
    if shd is None:
        return None
    return shd.get(f'{{{W}}}fill')