"""Inline content nodes embedded in Report.p()."""
import math2docx
from docx.text.paragraph import Paragraph


class Inline:
    """Base class for inline content nodes."""

    def render(self, para: Paragraph) -> None:
        raise NotImplementedError


class Bold(Inline):
    def __init__(self, text: str) -> None:
        self.text = text

    def render(self, para: Paragraph) -> None:
        para.add_run(self.text).bold = True


class Italic(Inline):
    def __init__(self, text: str) -> None:
        self.text = text

    def render(self, para: Paragraph) -> None:
        para.add_run(self.text).italic = True


class Formula(Inline):
    def __init__(self, latex: str) -> None:
        self.latex = latex

    def render(self, para: Paragraph) -> None:
        math2docx.add_math(para, self.latex)


def b(text: str) -> Inline:
    """Bold inline node for use inside Report.p()."""
    return Bold(text)


def i(text: str) -> Inline:
    """Italic inline node for use inside Report.p()."""
    return Italic(text)


def f(latex: str) -> Inline:
    """Inline formula node for use inside Report.p()."""
    return Formula(latex)