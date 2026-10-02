"""Unified formula accessor.

One name covers both contexts:

    p('formula: ', f('E = mc^2'))     # inline — returns an Inline node
    f.block('E = mc^2')               # block  — adds a standalone paragraph

A bare call returns an Inline. The .block() method adds a paragraph
to the current Report. This keeps the API surface small: users never
have to remember two names for the same concept.
"""
from typing import Optional

from ..inline import Formula
from ..styles import AlignLiteral
from ._state import current


class _FormulaAccessor:
    """Callable that yields an inline Formula; has a .block() method.

    The class is not meant to be instantiated by users. A singleton
    `f` is exported from the writer package.
    """

    def __call__(self, latex: str) -> Formula:
        """Return an inline Formula node.

        Use inside p(...), quote(...) or any method that accepts
        inline nodes. Does not modify the document.
        """
        return Formula(latex)

    def block(
        self,
        latex: str,
        *,
        align: Optional[AlignLiteral] = None,
        number: bool = False,
    ) -> None:
        """Add a block-level formula as its own paragraph.

        Args:
            latex: LaTeX source.
            align: local alignment override. None falls back to the
                resolved config (StylesConfig.formula, then the
                global StylesConfig.align).
            number: if True, the formula gets a right-aligned number
                "(1)", "(2)", ... in the same paragraph. Unnumbered
                formulas do not consume the counter.

        Returns:
            None. This is a terminal operation.
        """
        current().f(latex, align=align, number=number)


f = _FormulaAccessor()