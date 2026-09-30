"""Inline content nodes embedded in Report.p()."""
from typing import Union

import math2docx
from docx.enum.text import WD_COLOR_INDEX
from docx.shared import RGBColor
from docx.text.paragraph import Paragraph

from .._xml import add_hyperlink


RGB = tuple[int, int, int]

# String name -> WD_COLOR_INDEX. Kept small and explicit; users who
# need other shades can pass a WD_COLOR_INDEX member directly.
_HIGHLIGHT_COLORS = {
    'yellow': WD_COLOR_INDEX.YELLOW,
    'green': WD_COLOR_INDEX.GREEN,
    'cyan': WD_COLOR_INDEX.CYAN,
    'magenta': WD_COLOR_INDEX.MAGENTA,
    'blue': WD_COLOR_INDEX.BLUE,
    'red': WD_COLOR_INDEX.RED,
    'gray': WD_COLOR_INDEX.GRAY_25,
}


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


class Underline(Inline):
    def __init__(self, text: str) -> None:
        self.text = text

    def render(self, para: Paragraph) -> None:
        para.add_run(self.text).underline = True


class Strike(Inline):
    def __init__(self, text: str) -> None:
        self.text = text

    def render(self, para: Paragraph) -> None:
        para.add_run(self.text).font.strike = True


class Sup(Inline):
    def __init__(self, text: str) -> None:
        self.text = text

    def render(self, para: Paragraph) -> None:
        para.add_run(self.text).font.superscript = True


class Sub(Inline):
    def __init__(self, text: str) -> None:
        self.text = text

    def render(self, para: Paragraph) -> None:
        para.add_run(self.text).font.subscript = True


class Color(Inline):
    def __init__(self, text: str, rgb: RGB) -> None:
        self.text = text
        self.rgb = rgb

    def render(self, para: Paragraph) -> None:
        run = para.add_run(self.text)
        run.font.color.rgb = RGBColor(*self.rgb)


class Highlight(Inline):
    def __init__(self, text: str,
                 color: Union[str, WD_COLOR_INDEX] = 'yellow') -> None:
        self.text = text
        if isinstance(color, str):
            key = color.lower()
            if key not in _HIGHLIGHT_COLORS:
                raise ValueError(
                    f"unknown highlight color {color!r}; "
                    f"expected one of {sorted(_HIGHLIGHT_COLORS)} "
                    f"or a WD_COLOR_INDEX member"
                )
            self.color = _HIGHLIGHT_COLORS[key]
        else:
            self.color = color

    def render(self, para: Paragraph) -> None:
        run = para.add_run(self.text)
        run.font.highlight_color = self.color


class Formula(Inline):
    def __init__(self, latex: str) -> None:
        self.latex = latex

    def render(self, para: Paragraph) -> None:
        math2docx.add_math(para, self.latex)


class Link(Inline):
    def __init__(self, text: str, url: str) -> None:
        self.text = text
        self.url = url

    def render(self, para: Paragraph) -> None:
        add_hyperlink(para, self.text, self.url)


# ---------- factory functions ----------

def b(text: str) -> Inline:
    """Bold inline node."""
    return Bold(text)


def i(text: str) -> Inline:
    """Italic inline node."""
    return Italic(text)


def u(text: str) -> Inline:
    """Underline inline node."""
    return Underline(text)


def s(text: str) -> Inline:
    """Strikethrough inline node."""
    return Strike(text)


def sup(text: str) -> Inline:
    """Superscript inline node."""
    return Sup(text)


def sub(text: str) -> Inline:
    """Subscript inline node."""
    return Sub(text)


def color(text: str, rgb: RGB) -> Inline:
    """Colored inline node. `rgb` is an (r, g, b) tuple in 0..255."""
    return Color(text, rgb)


def highlight(text: str,
              color: Union[str, WD_COLOR_INDEX] = 'yellow') -> Inline:
    """Highlighted inline node.

    `color` is either a name from {yellow, green, cyan, magenta, blue,
    red, gray} or a `WD_COLOR_INDEX` member.
    """
    return Highlight(text, color)


def f(latex: str) -> Inline:
    """Inline formula node."""
    return Formula(latex)


def link(text: str, url: str) -> Inline:
    """Hyperlink inline node."""
    return Link(text, url)