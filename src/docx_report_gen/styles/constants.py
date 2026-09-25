"""Shared constants for style configuration and application."""
from docx.enum.text import WD_ALIGN_PARAGRAPH


ALIGN = {
    None: None,
    'left': WD_ALIGN_PARAGRAPH.LEFT,
    'center': WD_ALIGN_PARAGRAPH.CENTER,
    'right': WD_ALIGN_PARAGRAPH.RIGHT,
    'justify': WD_ALIGN_PARAGRAPH.JUSTIFY,
}

# Paragraph style names for captions. Created automatically by apply()
# if they do not yet exist in the document.
CAPTION_STYLE_NAME = 'ReportCaption'            # tables
IMAGE_CAPTION_STYLE_NAME = 'ReportImageCaption' # images