"""Code block mixin."""
from .._xml import set_paragraph_shading
from ..styles import ALIGN, CODE_STYLE_NAME, resolve_code
from ._base import DocMixin


class CodeMixin(DocMixin):
    """Adds code() to Report.

    Each source line becomes its own paragraph, so that long code
    blocks can break across pages naturally.
    """

    def code(self, text, language=None, align=None):
        """Insert a monospace code block.

        Args:
            text: the code text; newlines split it into paragraphs.
            language: recorded for future use; Word has no built-in
                syntax highlighting, so it does not affect rendering.
            align: alignment override for every line.
        """
        resolved = resolve_code(self.config, {'align': align})
        lines = str(text).splitlines() or ['']
        for line in lines:
            para = self.doc.add_paragraph(style=CODE_STYLE_NAME)
            para.alignment = ALIGN[resolved.align]
            para.add_run(line if line else ' ')
            if resolved.background:
                set_paragraph_shading(para, resolved.background)
        return self