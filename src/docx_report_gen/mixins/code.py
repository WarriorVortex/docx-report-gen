"""Code block mixin."""
from .._xml import set_paragraph_shading
from ..styles import CODE_STYLE_NAME, resolve_code
from ._base import DocMixin
from .utils import apply_layout, check_align


class CodeMixin(DocMixin):
    """Adds code() to Report.

    Each source line becomes its own paragraph, so that long code
    blocks can break across pages naturally.
    """

    def code(self, text, language=None, align=None,
             line_spacing=None, space_before=None, space_after=None,
             left_indent=None):
        """Insert a monospace code block.

        Args:
            text: the code text; newlines split it into paragraphs.
            language: recorded for future use; Word has no built-in
                syntax highlighting, so it does not affect rendering.
            align, line_spacing, space_before, space_after, left_indent:
                local layout overrides.
        """
        check_align(align, where='code')
        local = {
            'align': align,
            'line_spacing': line_spacing,
            'space_before': space_before,
            'space_after': space_after,
            'left_indent': left_indent,
        }
        resolved = resolve_code(self.config, local)
        lines = str(text).splitlines() or ['']
        for line in lines:
            para = self.doc.add_paragraph(style=CODE_STYLE_NAME)
            apply_layout(para, resolved)
            para.add_run(line if line else ' ')
            if resolved.background:
                set_paragraph_shading(para, resolved.background)
        return self