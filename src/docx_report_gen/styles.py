"""Document style configuration."""
from docx.shared import Pt, RGBColor, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH


ALIGN = {
    None: None,
    'left': WD_ALIGN_PARAGRAPH.LEFT,
    'center': WD_ALIGN_PARAGRAPH.CENTER,
    'right': WD_ALIGN_PARAGRAPH.RIGHT,
    'justify': WD_ALIGN_PARAGRAPH.JUSTIFY,
}


def configure_fonts(doc, font, size, h_sizes):
    """Document style configuration."""
    normal = doc.styles['Normal']
    normal.font.name = font
    normal.font.size = Pt(size)

    for i, hsize in enumerate(h_sizes, start=1):
        s = doc.styles[f'Heading {i}']
        s.font.name = font
        s.font.size = Pt(hsize)
        s.font.color.rgb = RGBColor(0, 0, 0)
        s.font.bold = True


def set_margins(doc, top, right, bottom, left):
    """Set page margins in centimeters."""
    for section in doc.sections:
        section.top_margin = Cm(top)
        section.right_margin = Cm(right)
        section.bottom_margin = Cm(bottom)
        section.left_margin = Cm(left)