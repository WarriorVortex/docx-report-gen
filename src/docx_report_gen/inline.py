"""Inline content nodes embedded in Report.p()."""
import math2docx


class Inline:
    """Base class for inline content nodes."""

    def render(self, para):
        raise NotImplementedError


class Bold(Inline):
    def __init__(self, text):
        self.text = text

    def render(self, para):
        para.add_run(self.text).bold = True


class Italic(Inline):
    def __init__(self, text):
        self.text = text

    def render(self, para):
        para.add_run(self.text).italic = True


class Formula(Inline):
    def __init__(self, latex):
        self.latex = latex

    def render(self, para):
        math2docx.add_math(para, self.latex)


def b(text):
    """Bold inline node for use inside Report.p()."""
    return Bold(text)


def i(text):
    """Italic inline node for use inside Report.p()."""
    return Italic(text)


def f(latex):
    """Inline formula node for use inside Report.p()."""
    return Formula(latex)