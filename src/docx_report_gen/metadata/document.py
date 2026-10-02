"""Document metadata dataclass."""
from dataclasses import dataclass
from typing import Optional


@dataclass
class DocumentMetadata:
    """Core properties written into the docx file.

    All fields are optional. None means 'leave the Word default',
    which is typically an empty string.
    """
    author: Optional[str] = None
    title: Optional[str] = None
    subject: Optional[str] = None
    keywords: Optional[str] = None
    comments: Optional[str] = None
    category: Optional[str] = None
    last_modified_by: Optional[str] = None