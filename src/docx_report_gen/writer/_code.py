"""Unified code accessor.

One name covers both contexts:

    p('Function ', code('print'), ' outputs text')   # inline — returns Inline
    code.block('def f(x):\\n    return x')            # block  — adds paragraph

A bare call returns a CodeInline node. The .block() method adds a
shaded, monospace code block to the current Report. The two modes
differ in structure — inline is a plain run, block is a paragraph
with background and line handling — but share a name, because users
think of them as "code" in two contexts.
"""
from typing import Optional

from ..inline import CodeInline
from ..styles import AlignLiteral
from ._state import current


class _CodeAccessor:
    """Callable that yields an inline CodeInline; has a .block() method.

    Not meant to be instantiated by users. A singleton `code` is
    exported from the writer package.
    """

    def __call__(self, text: str) -> CodeInline:
        """Return an inline CodeInline node.

        Use inside p(...), quote(...) or any method that accepts
        inline nodes. Does not modify the document.
        """
        return CodeInline(text)

    def block(
        self,
        text: str,
        language: Optional[str] = None,
        align: Optional[AlignLiteral] = None,
        line_spacing: Optional[float] = None,
        space_before: Optional[int] = None,
        space_after: Optional[int] = None,
        left_indent: Optional[float] = None,
    ) -> None:
        """Add a monospace code block.

        Args:
            text: code text. Newlines split it into separate paragraphs
                so long blocks can break across pages naturally.
            language: recorded for future use; Word has no built-in
                syntax highlighting.
            align, line_spacing, space_before, space_after, left_indent:
                local layout overrides.

        Returns:
            None. This is a terminal operation.
        """
        current().code(
            text,
            language=language,
            align=align,
            line_spacing=line_spacing,
            space_before=space_before,
            space_after=space_after,
            left_indent=left_indent,
        )


code = _CodeAccessor()