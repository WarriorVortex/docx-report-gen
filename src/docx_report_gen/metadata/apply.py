"""Apply DocumentMetadata to a python-docx Document."""
from .._docx import DocumentProtocol
from .document import DocumentMetadata


_METADATA_FIELDS: tuple[str, ...] = (
    'author',
    'title',
    'subject',
    'keywords',
    'comments',
    'category',
    'last_modified_by',
)


def apply_metadata(doc: DocumentProtocol,
                   metadata: DocumentMetadata) -> None:
    """Copy non-None metadata fields into the document's core properties."""
    props = doc.core_properties
    for name in _METADATA_FIELDS:
        value = getattr(metadata, name)
        if value is not None:
            setattr(props, name, value)