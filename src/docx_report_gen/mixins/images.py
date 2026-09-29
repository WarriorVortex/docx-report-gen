"""Image mixin with optional captions."""
from pathlib import Path

from docx.shared import Cm

from ..styles import (
    ALIGN, IMAGE_CAPTION_STYLE_NAME,
    resolve_image, resolve_image_caption,
)
from ._base import DocMixin
from .utils import render_caption


class ImageMixin(DocMixin):
    """Adds img() to Report.

    Captioned images use a separate counter from tables: the first
    captioned image becomes 1, the next 2, and so on. Uncaptered
    images do not consume a number.
    """

    _image_counter = 0

    def img(self, path, caption=None, caption_align=None,
            width=None, align=None):
        """Insert an image, optionally followed by a numbered caption.

        Args:
            path: path to the image file.
            caption: caption text; None disables the caption.
            caption_align: local alignment override for the caption.
            width: image width in cm (or a docx.shared.Length object).
                None falls back to StylesConfig.image.width or native size.
            align: alignment of the image paragraph; None falls back to
                StylesConfig.image.align or the global StylesConfig.align.
        """
        ist = resolve_image(self.config, {'align': align, 'width': width})

        para = self.doc.add_paragraph()
        para.alignment = ALIGN[ist.align]
        run = para.add_run()
        kwargs = {}
        if ist.width is not None:
            kwargs['width'] = (
                Cm(ist.width) if isinstance(ist.width, (int, float))
                else ist.width
            )
        run.add_picture(str(path), **kwargs)

        if caption is not None:
            self._image_counter += 1
            para.paragraph_format.keep_with_next = True
            cs = resolve_image_caption(self.config, {'align': caption_align})
            render_caption(
                self.doc, cs, IMAGE_CAPTION_STYLE_NAME,
                self._image_counter, caption,
            )
        return self