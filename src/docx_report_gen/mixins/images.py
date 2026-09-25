"""Image mixin with optional captions."""
from pathlib import Path

from docx.shared import Cm

from ..styles import ALIGN, IMAGE_CAPTION_STYLE_NAME
from ._base import DocMixin
from .utils import render_caption


class ImageMixin(DocMixin):
    """Adds img() to Report.

    Captioned images are numbered with a separate counter from tables:
    the first captioned image becomes 1, the next 2, and so on.
    Uncaptered images do not consume a number.
    """

    _image_counter = 0

    def img(self, path: str | Path, caption: str | None = None,
            width: float | None = None, align: str = 'center'):
        """Insert an image, optionally followed by a numbered caption."""
        para = self.doc.add_paragraph()
        para.alignment = ALIGN[align]
        run = para.add_run()
        kwargs = {}
        if width is not None:
            kwargs['width'] = (
                Cm(width) if isinstance(width, (int, float)) else width
            )
        run.add_picture(str(path), **kwargs)

        if caption is not None:
            self._image_counter += 1
            para.paragraph_format.keep_with_next = True
            render_caption(
                self.doc, self.config.image_caption,
                IMAGE_CAPTION_STYLE_NAME,
                self._image_counter, caption,
            )
        return self