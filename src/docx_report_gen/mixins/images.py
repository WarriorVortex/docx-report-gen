"""Image mixin with optional captions."""
from pathlib import Path

from docx.shared import Cm

from ..styles import (
    ALIGN, IMAGE_CAPTION_STYLE_NAME, SEQ_FIGURE,
    resolve_image, resolve_image_caption,
)
from ._base import DocMixin
from .bookmarks import BookmarkMixin
from .utils import check_align, render_caption


class ImageMixin(BookmarkMixin, DocMixin):
    """Adds img() to Report.

    Captioned images are numbered by a Word SEQ field — one counter
    for all images in the document, independent from the table counter.
    """

    def img(self, path, caption=None, caption_align=None, name=None,
            width=None, align=None):
        """Insert an image, optionally followed by a numbered caption.

        Args:
            path: path to the image file.
            caption: caption text; None disables the caption.
            caption_align: local alignment override for the caption.
            name: optional bookmark name for cross-referencing via
                Report.ref(name). Must not contain whitespace.
            width: image width in cm (or a docx.shared.Length object).
                None falls back to StylesConfig.image.width or native size.
            align: alignment of the image paragraph; None falls back to
                StylesConfig.image.align or the global StylesConfig.align.
        """
        file_path = Path(path)
        if not file_path.exists():
            raise FileNotFoundError(
                f'img(): image file not found: {file_path}'
            )
        check_align(align, where='img')
        check_align(caption_align, where='img caption')

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
        run.add_picture(str(file_path), **kwargs)

        if caption is not None:
            para.paragraph_format.keep_with_next = True
            cs = resolve_image_caption(self.config, {'align': caption_align})
            bookmark_name, bookmark_id = self._prepare_bookmark(
                name, kind='image',
            )
            render_caption(
                self.doc, cs, IMAGE_CAPTION_STYLE_NAME,
                caption=caption, seq_name=SEQ_FIGURE,
                bookmark_name=bookmark_name, bookmark_id=bookmark_id,
            )
        return self