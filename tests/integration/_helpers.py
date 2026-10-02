"""Helpers for integration tests that inspect the full docx package."""
import zipfile

from lxml import etree


W = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
M = 'http://schemas.openxmlformats.org/officeDocument/2006/math'
PKG_REL = 'http://schemas.openxmlformats.org/package/2006/relationships'


def read_part(path, part_name):
    """Return raw bytes of a part inside the .docx archive."""
    with zipfile.ZipFile(path) as zf:
        return zf.read(part_name)


def xml_part(path, part_name):
    return etree.fromstring(read_part(path, part_name))


def all_text(path):
    """Concatenate every <w:t> in word/document.xml."""
    xml = xml_part(path, 'word/document.xml')
    return ''.join(el.text or '' for el in xml.iter(f'{{{W}}}t'))


def count_omath(path):
    xml = xml_part(path, 'word/document.xml')
    return len(xml.findall(f'.//{{{M}}}oMath'))


def count_instr_fields(path, name):
    """Count instrText elements containing `name` as a substring."""
    xml = xml_part(path, 'word/document.xml')
    return sum(
        1 for el in xml.iter(f'{{{W}}}instrText')
        if name in (el.text or '')
    )


def bookmark_names(path):
    xml = xml_part(path, 'word/document.xml')
    return [
        el.get(f'{{{W}}}name')
        for el in xml.findall(f'.//{{{W}}}bookmarkStart')
        if el.get(f'{{{W}}}name')
    ]


def hyperlink_targets(path):
    """External hyperlink URLs registered in document.xml.rels."""
    rels = xml_part(path, 'word/_rels/document.xml.rels')
    hyperlink_type = (
        'http://schemas.openxmlformats.org/officeDocument/2006'
        '/relationships/hyperlink'
    )
    return [
        rel.get('Target')
        for rel in rels.findall(f'{{{PKG_REL}}}Relationship')
        if rel.get('Type') == hyperlink_type
    ]


def list_parts(path):
    with zipfile.ZipFile(path) as zf:
        return set(zf.namelist())