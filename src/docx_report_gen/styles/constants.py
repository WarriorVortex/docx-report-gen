"""Shared constants for style configuration and application."""
from docx.enum.text import WD_ALIGN_PARAGRAPH


ALIGN = {
    None: None,
    'left': WD_ALIGN_PARAGRAPH.LEFT,
    'center': WD_ALIGN_PARAGRAPH.CENTER,
    'right': WD_ALIGN_PARAGRAPH.RIGHT,
    'justify': WD_ALIGN_PARAGRAPH.JUSTIFY,
}

# Paragraph style names for custom elements.
CAPTION_STYLE_NAME = 'ReportCaption'
IMAGE_CAPTION_STYLE_NAME = 'ReportImageCaption'
CODE_STYLE_NAME = 'ReportCode'
QUOTE_STYLE_NAME = 'ReportQuote'

# Word built-in list styles, by nesting level (1..3).
LIST_BULLET_STYLES = ('List Bullet', 'List Bullet 2', 'List Bullet 3')
LIST_NUMBER_STYLES = ('List Number', 'List Number 2', 'List Number 3')

# SEQ field names — one counter per category.
SEQ_TABLE = 'Table'
SEQ_FIGURE = 'Figure'

# Bookmark names are prefixed to avoid collisions with user-defined
# bookmarks in the same document.
BOOKMARK_PREFIX = '_Ref_'