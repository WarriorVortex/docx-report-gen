"""Apply DocumentMetadata to a python-docx Document."""
from docx import Document

from .document import DocumentMetadata


# Fields copied verbatim into core_properties. Kept explicit so that
# adding a field to DocumentMetadata is a conscious decision, not an
# accident of attribute-name matching.
_METADATA_FIELDS = (
    'author',
    'title',
    'subject',
    'keywords',
    'comments',
    'category',
    'last_modified_by',
)


def apply_metadata(doc: Document, metadata: DocumentMetadata) -> None:
    """Copy non-None metadata fields into the document's core properties."""
    props = doc.core_properties
    for name in _METADATA_FIELDS:
        value = getattr(metadata, name)
        if value is not None:
            setattr(props, name, value)