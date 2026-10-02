"""Image mixin with optional captions."""
from pathlib import Path
from typing import Optional, Union

from docx.shared import Cm, Length

from ..styles import (
    ALIGN, IMAGE_CAPTION_STYLE_NAME, SEQ_FIGURE, AlignLiteral,
    PathLike, resolve_image, resolve_image_caption,
)
from ._base import DocMixin
from .bookmarks import BookmarkMixin
from ._utils import check_align, render_caption


class ImageMixin(BookmarkMixin, DocMixin):
    """Adds img() to Report."""

    def img(
        self,
        path: PathLike,
        caption: Optional[str] = None,
        caption_align: Optional[AlignLiteral] = None,
        name: Optional[str] = None,
        width: Optional[Union[float, Length]] = None,
        align: Optional[AlignLiteral] = None,
    ) -> 'ImageMixin':
        """Insert an image, optionally followed by a numbered caption."""
        file_path = Path(path)
        if not file_path.exists():
            raise FileNotFoundError(
                f'img(): image file not found: {file_path}'
            )
        check_align(align, where='img')
        check_align(caption_align, where='img caption')

        ist = resolve_image(self.config, {'align': align, 'width': width})

        para = self.doc.add_paragraph()
        alignment = ALIGN[ist.align]
        if alignment is not None:
            para.alignment = alignment
        run = para.add_run()

        # Length subclasses int, so a Length instance would match the
        # (int, float) branch below if checked first. Check Length
        # before numbers: Length is passed through as-is (it already
        # carries a unit), plain numbers are interpreted as centimeters.
        if ist.width is None:
            run.add_picture(str(file_path))
        elif isinstance(ist.width, Length):
            run.add_picture(str(file_path), width=ist.width)
        elif isinstance(ist.width, (int, float)):
            run.add_picture(str(file_path), width=Cm(ist.width))
        else:
            run.add_picture(str(file_path), width=ist.width)

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