"""Shared constants for style configuration and application."""
from docx.enum.text import WD_ALIGN_PARAGRAPH


ALIGN = {
    None: None,
    'left': WD_ALIGN_PARAGRAPH.LEFT,
    'center': WD_ALIGN_PARAGRAPH.CENTER,
    'right': WD_ALIGN_PARAGRAPH.RIGHT,
    'justify': WD_ALIGN_PARAGRAPH.JUSTIFY,
}

# Paragraph style names for custom elements. Created by apply()
# if they do not already exist in the document.
CAPTION_STYLE_NAME = 'ReportCaption'            # tables
IMAGE_CAPTION_STYLE_NAME = 'ReportImageCaption' # images
CODE_STYLE_NAME = 'ReportCode'                  # code blocks
QUOTE_STYLE_NAME = 'ReportQuote'                # block quotes

# Word built-in list styles, by nesting level (1..3).
LIST_BULLET_STYLES = ('List Bullet', 'List Bullet 2', 'List Bullet 3')
LIST_NUMBER_STYLES = ('List Number', 'List Number 2', 'List Number 3')